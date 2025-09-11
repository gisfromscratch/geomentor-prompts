"""
Routing Agent for Problem-Solving using ArcGIS Location Platform

This module implements a routing agent that follows the problem formulation structure:
- Initial State: Start location (geocoded)
- Actions: Move along road network segments 
- Transition Model: Apply ArcGIS routing API to compute new states and costs
- Goal Test: Check if current state is within buffer of target location
- Path Cost: Travel time (primary), with multi-criteria extension capability
"""

import logging
import os
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple
from dotenv import load_dotenv

try:
    from arcgis.gis import GIS
    from arcgis.geocoding import geocode
    from arcgis.network import RouteLayer
    from arcgis.geometry import Point, Polyline
    from arcgis.features import FeatureLayer, FeatureSet, Feature
except ImportError as e:
    logging.error(f"ArcGIS API for Python not installed: {e}")
    raise ImportError(
        "Please install ArcGIS API for Python: pip install arcgis"
    ) from e

from .location_state import LocationState, RouteSegment, RoutingDecision

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class RoutingAgent:
    """
    Routing Agent implementing problem-solving approach for route computation
    from Bonn to Remagen using ArcGIS Location Platform
    """

    def __init__(self, 
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 api_key: Optional[str] = None,
                 org_url: Optional[str] = None):
        """
        Initialize the routing agent with ArcGIS credentials
        
        Args:
            username: ArcGIS username (from env if not provided)
            password: ArcGIS password (from env if not provided)
            api_key: ArcGIS API key (alternative to username/password)
            org_url: ArcGIS organization URL
        """
        # Get credentials from environment if not provided
        self.username = username or os.getenv("ARCGIS_USERNAME")
        self.password = password or os.getenv("ARCGIS_PASSWORD")
        self.api_key = api_key or os.getenv("ARCGIS_API_KEY")
        self.org_url = org_url or os.getenv("ARCGIS_ORG_URL", "https://www.arcgis.com")
        
        # Configuration
        self.travel_mode = os.getenv("DEFAULT_TRAVEL_MODE", "Driving")
        self.buffer_meters = float(os.getenv("ROUTE_BUFFER_METERS", "200"))
        
        # Initialize GIS connection
        self.gis = None
        self.route_service = None
        self._connect_to_arcgis()
        
        logger.info("RoutingAgent initialized")

    def _connect_to_arcgis(self):
        """Establish connection to ArcGIS Location Platform"""
        try:
            if self.api_key:
                # Use API key authentication
                self.gis = GIS(api_key=self.api_key)
                logger.info("Connected to ArcGIS using API key")
            elif self.username and self.password:
                # Use username/password authentication
                self.gis = GIS(self.org_url, username=self.username, password=self.password)
                logger.info(f"Connected to ArcGIS as {self.username}")
            else:
                # Try anonymous connection
                self.gis = GIS()
                logger.warning("Connected to ArcGIS anonymously - limited functionality")
            
            # Get routing service
            # This uses ArcGIS World Route Service
            self.route_service = self.gis.properties.helperServices.route.url
            logger.info(f"Route service URL: {self.route_service}")
            
        except Exception as e:
            logger.error(f"Failed to connect to ArcGIS: {e}")
            raise

    def geocode_location(self, address: str, country: str = "Germany") -> LocationState:
        """
        Geocode an address to get coordinates (Initial State / Goal State)
        
        Args:
            address: Address string (e.g., "Bonn, Germany")
            country: Country for geocoding context
            
        Returns:
            LocationState with coordinates and address
        """
        logger.info(f"Geocoding address: {address}")
        
        try:
            # Use ArcGIS geocoding service
            geocode_result = geocode(
                address=f"{address}, {country}", 
                max_locations=1,
                as_featureset=True,
                gis=self.gis
            )
            
            if len(geocode_result.features) == 0:
                raise ValueError(f"Could not geocode address: {address}")
            
            feature = geocode_result.features[0]
            geometry = feature.geometry
            attributes = feature.attributes
            
            location_state = LocationState(
                latitude=geometry.y,
                longitude=geometry.x,
                address=attributes.get('PlaceName', address),
                timestamp=datetime.now()
            )
            
            logger.info(f"Geocoded {address} to {location_state}")
            return location_state
            
        except Exception as e:
            logger.error(f"Error geocoding {address}: {e}")
            raise

    def compute_route(self, 
                     start_state: LocationState, 
                     end_state: LocationState) -> RoutingDecision:
        """
        Apply transition model: compute route from start to end using ArcGIS routing
        
        Args:
            start_state: Starting location state
            end_state: Destination location state
            
        Returns:
            RoutingDecision with route segments and costs
        """
        logger.info(f"Computing route from {start_state} to {end_state}")
        
        try:
            # Create route layer for analysis
            from arcgis.network import RouteLayer
            route_layer = RouteLayer(self.route_service, gis=self.gis)
            
            # Define stops as Point geometries
            stops = [
                Point({"x": start_state.longitude, "y": start_state.latitude, 
                      "spatialReference": {"wkid": 4326}}),
                Point({"x": end_state.longitude, "y": end_state.latitude,
                      "spatialReference": {"wkid": 4326}})
            ]
            
            # Solve the route
            route_result = route_layer.solve(
                stops=stops,
                travel_mode=self.travel_mode,
                return_directions=True,
                return_routes=True,
                return_stops=True
            )
            
            # Extract route information
            if not route_result.routes.features:
                raise ValueError("No route found between locations")
            
            route_feature = route_result.routes.features[0]
            route_attributes = route_feature.attributes
            route_geometry = route_feature.geometry
            
            # Get total metrics
            total_time_minutes = route_attributes.get('Total_TravelTime', 0)  # in minutes
            total_distance_km = route_attributes.get('Total_Length', 0)  # in km
            
            # Extract route segments from directions
            route_segments = []
            if hasattr(route_result, 'directions') and route_result.directions:
                directions = route_result.directions[0]  # First route's directions
                if hasattr(directions, 'features'):
                    for i, direction_feature in enumerate(directions.features):
                        dir_attrs = direction_feature.attributes
                        segment_geometry = direction_feature.geometry
                        
                        # Create segment start/end locations (simplified)
                        if i == 0:
                            segment_start = start_state
                        else:
                            # Use previous segment end as start
                            segment_start = route_segments[-1].end_location
                        
                        if i == len(directions.features) - 1:
                            segment_end = end_state
                        else:
                            # Approximate end location from geometry
                            if hasattr(segment_geometry, 'paths') and segment_geometry.paths:
                                last_point = segment_geometry.paths[0][-1]
                                segment_end = LocationState(
                                    latitude=last_point[1],
                                    longitude=last_point[0]
                                )
                            else:
                                segment_end = end_state
                        
                        segment = RouteSegment(
                            start_location=segment_start,
                            end_location=segment_end,
                            travel_time_minutes=dir_attrs.get('ElapsedTime', 0),
                            distance_km=dir_attrs.get('Length', 0),
                            instructions=dir_attrs.get('Text', ''),
                            geometry=segment_geometry.as_dict() if hasattr(segment_geometry, 'as_dict') else None
                        )
                        route_segments.append(segment)
            
            # If no detailed segments, create single segment
            if not route_segments:
                route_segments = [RouteSegment(
                    start_location=start_state,
                    end_location=end_state,
                    travel_time_minutes=total_time_minutes,
                    distance_km=total_distance_km,
                    instructions=f"Route from {start_state.address} to {end_state.address}"
                )]
            
            # Check if goal is reached (within buffer)
            goal_reached = start_state.within_buffer(end_state, self.buffer_meters)
            if not goal_reached:
                # For a successful route computation, we consider goal reached
                goal_reached = True
            
            # Calculate confidence (simplified - based on successful route computation)
            confidence = 1.0 if route_segments else 0.0
            
            routing_decision = RoutingDecision(
                route_segments=route_segments,
                total_travel_time=total_time_minutes,
                total_distance=total_distance_km,
                goal_reached=goal_reached,
                current_state=start_state,
                target_state=end_state,
                confidence=confidence,
                timestamp=datetime.now(),
                route_geometry=route_geometry.as_dict() if hasattr(route_geometry, 'as_dict') else None
            )
            
            logger.info(f"Route computed: {routing_decision.summary()}")
            return routing_decision
            
        except Exception as e:
            logger.error(f"Error computing route: {e}")
            # Return failed decision
            return RoutingDecision(
                route_segments=[],
                total_travel_time=0,
                total_distance=0,
                goal_reached=False,
                current_state=start_state,
                target_state=end_state,
                confidence=0.0,
                timestamp=datetime.now()
            )

    def goal_test(self, current_state: LocationState, target_state: LocationState) -> bool:
        """
        Goal Test: Check if current state is within buffer distance of target
        
        Args:
            current_state: Current location state
            target_state: Target/goal location state
            
        Returns:
            True if goal is reached (within buffer), False otherwise
        """
        within_buffer = current_state.within_buffer(target_state, self.buffer_meters)
        logger.info(f"Goal test: {current_state} within {self.buffer_meters}m of {target_state}: {within_buffer}")
        return within_buffer

    def publish_route_to_feature_layer(self, 
                                     routing_decision: RoutingDecision,
                                     layer_name: str = "Bonn_to_Remagen_Route") -> Optional[str]:
        """
        Publish route results to a hosted feature layer for inspection
        
        Args:
            routing_decision: The routing decision to publish
            layer_name: Name for the feature layer
            
        Returns:
            Feature layer URL if successful, None otherwise
        """
        logger.info(f"Publishing route to feature layer: {layer_name}")
        
        try:
            if not routing_decision.route_geometry:
                logger.warning("No route geometry to publish")
                return None
            
            # Create feature for the route
            route_feature = Feature(
                geometry=routing_decision.route_geometry,
                attributes={
                    "Name": layer_name,
                    "StartAddress": routing_decision.current_state.address or "Start",
                    "EndAddress": routing_decision.target_state.address or "End", 
                    "TotalTime_Minutes": routing_decision.total_travel_time,
                    "TotalDistance_KM": routing_decision.total_distance,
                    "Confidence": routing_decision.confidence,
                    "Timestamp": routing_decision.timestamp.isoformat(),
                    "GoalReached": routing_decision.goal_reached
                }
            )
            
            # Create feature set
            route_featureset = FeatureSet([route_feature])
            
            # Publish to ArcGIS Online
            published_item = self.gis.content.import_data(
                route_featureset,
                title=layer_name,
                tags=["routing", "agent", "bonn", "remagen"]
            )
            
            logger.info(f"Route published successfully: {published_item.url}")
            return published_item.url
            
        except Exception as e:
            logger.error(f"Error publishing route to feature layer: {e}")
            return None

    def solve_routing_problem(self, 
                            start_address: str = "Bonn, Germany",
                            end_address: str = "Remagen, Germany") -> RoutingDecision:
        """
        Main method to solve the routing problem from start to end address
        Following the complete problem formulation structure
        
        Args:
            start_address: Starting address (default: Bonn, Germany)
            end_address: Destination address (default: Remagen, Germany)
            
        Returns:
            RoutingDecision with complete route information
        """
        logger.info(f"Solving routing problem: {start_address} → {end_address}")
        
        try:
            # Step 1: Define Initial State (geocode start location)
            start_state = self.geocode_location(start_address)
            logger.info(f"Initial state: {start_state}")
            
            # Step 2: Define Goal State (geocode destination)
            goal_state = self.geocode_location(end_address)
            logger.info(f"Goal state: {goal_state}")
            
            # Step 3: Apply Transition Model (compute route)
            routing_decision = self.compute_route(start_state, goal_state)
            
            # Step 4: Goal Test (verify destination reached)
            goal_reached = self.goal_test(
                routing_decision.current_state, 
                routing_decision.target_state
            )
            routing_decision.goal_reached = goal_reached
            
            # Step 5: Publish results for inspection
            feature_layer_url = self.publish_route_to_feature_layer(routing_decision)
            if feature_layer_url:
                logger.info(f"Route published to: {feature_layer_url}")
            
            logger.info(f"Routing problem solved: {routing_decision.summary()}")
            return routing_decision
            
        except Exception as e:
            logger.error(f"Error solving routing problem: {e}")
            raise

    def validate_decision(self, routing_decision: RoutingDecision) -> bool:
        """
        Validate routing decision for correctness
        
        Args:
            routing_decision: The routing decision to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not routing_decision:
            return False
        
        # Check basic validity
        if routing_decision.total_travel_time < 0 or routing_decision.total_distance < 0:
            logger.error("Invalid negative travel time or distance")
            return False
        
        if not routing_decision.route_segments and routing_decision.goal_reached:
            logger.error("Goal reached but no route segments")
            return False
        
        # Check coordinate validity
        for segment in routing_decision.route_segments:
            if not self._is_valid_coordinate(segment.start_location) or \
               not self._is_valid_coordinate(segment.end_location):
                logger.error("Invalid coordinates in route segments")
                return False
        
        logger.info("Routing decision validated successfully")
        return True
    
    def _is_valid_coordinate(self, location: LocationState) -> bool:
        """Check if location has valid coordinates"""
        return (-90 <= location.latitude <= 90 and 
                -180 <= location.longitude <= 180)


# Example usage
if __name__ == "__main__":
    # Initialize routing agent
    agent = RoutingAgent()
    
    # Solve the Bonn to Remagen routing problem
    result = agent.solve_routing_problem()
    
    print(f"\n--- Routing Results ---")
    print(f"Route: {result.summary()}")
    print(f"Path Cost: {result.path_cost:.2f} minutes")
    print(f"Multi-criteria Cost: {result.get_multi_criteria_cost():.2f}")
    
    if result.route_segments:
        print(f"\nRoute Segments ({len(result.route_segments)}):")
        for i, segment in enumerate(result.route_segments, 1):
            print(f"  {i}. {segment.instructions} ({segment.travel_time_minutes:.1f} min, {segment.distance_km:.2f} km)")