"""
Mock/Demo Routing Agent for testing without ArcGIS dependencies

This version demonstrates the agent functionality using simulated data,
allowing testing and validation without requiring ArcGIS credentials.
"""

import logging
import math
from datetime import datetime
from typing import Optional, List, Dict, Any

from .location_state import LocationState, RouteSegment, RoutingDecision

logger = logging.getLogger(__name__)


class MockRoutingAgent:
    """
    Mock implementation of the Routing Agent for testing purposes
    
    This version simulates ArcGIS functionality to demonstrate the problem
    formulation approach without requiring ArcGIS credentials.
    """

    def __init__(self, buffer_meters: float = 200):
        """
        Initialize the mock routing agent
        
        Args:
            buffer_meters: Goal test buffer distance
        """
        self.buffer_meters = buffer_meters
        self.travel_mode = "Driving"
        
        # Known locations for demo (approximate coordinates)
        self._known_locations = {
            "bonn, germany": LocationState(50.7374, 7.0982, "Bonn, DEU"),
            "remagen, germany": LocationState(50.5791, 7.2281, "Remagen, DEU"),
            "köln, germany": LocationState(50.9375, 6.9603, "Köln, DEU"),
            "düsseldorf, germany": LocationState(51.2277, 6.7735, "Düsseldorf, DEU"),
        }
        
        logger.info("MockRoutingAgent initialized (no ArcGIS required)")

    def geocode_location(self, address: str, country: str = "Germany") -> LocationState:
        """
        Mock geocoding using predefined locations
        
        Args:
            address: Address string
            country: Country (ignored in mock)
            
        Returns:
            LocationState with coordinates
        """
        address_key = address.lower()
        
        if address_key in self._known_locations:
            location = self._known_locations[address_key]
            logger.info(f"Mock geocoded {address} to {location}")
            return location
        else:
            # For unknown addresses, generate approximate coordinates
            # This is just for demo - in reality would fail
            logger.warning(f"Unknown address {address}, using approximate coordinates")
            return LocationState(50.0, 7.0, address)

    def compute_route(self, start_state: LocationState, end_state: LocationState) -> RoutingDecision:
        """
        Mock route computation using simplified calculations
        
        Args:
            start_state: Starting location
            end_state: Destination location
            
        Returns:
            RoutingDecision with simulated route
        """
        logger.info(f"Mock computing route from {start_state} to {end_state}")
        
        # Calculate straight-line distance
        distance_m = start_state.distance_to(end_state)
        distance_km = distance_m / 1000
        
        # Simulate route by adding 20% for actual roads (rough approximation)
        actual_distance_km = distance_km * 1.2
        
        # Estimate travel time: average 50 km/h in city, 80 km/h on highway
        # For German cities, assume mixed driving
        avg_speed_kmh = 60
        travel_time_hours = actual_distance_km / avg_speed_kmh
        travel_time_minutes = travel_time_hours * 60
        
        # Create simplified route segments (just start -> end)
        route_segments = [
            RouteSegment(
                start_location=start_state,
                end_location=end_state,
                travel_time_minutes=travel_time_minutes,
                distance_km=actual_distance_km,
                instructions=f"Drive from {start_state.address} to {end_state.address}",
                geometry={"type": "LineString", "coordinates": [
                    [start_state.longitude, start_state.latitude],
                    [end_state.longitude, end_state.latitude]
                ]}
            )
        ]
        
        # Mock route geometry
        route_geometry = {
            "type": "LineString",
            "coordinates": [
                [start_state.longitude, start_state.latitude],
                [end_state.longitude, end_state.latitude]
            ]
        }
        
        # Goal test: for a successfully computed route, we consider goal achieved
        # The buffer test is primarily for validating if we're already at destination
        goal_reached = True  # We computed a valid route to destination
        confidence = 0.9  # High confidence in mock route
        
        routing_decision = RoutingDecision(
            route_segments=route_segments,
            total_travel_time=travel_time_minutes,
            total_distance=actual_distance_km,
            goal_reached=goal_reached,
            current_state=start_state,
            target_state=end_state,
            confidence=confidence,
            timestamp=datetime.now(),
            route_geometry=route_geometry
        )
        
        logger.info(f"Mock route computed: {routing_decision.summary()}")
        return routing_decision

    def goal_test(self, current_state: LocationState, target_state: LocationState) -> bool:
        """
        Goal test implementation (same as real agent)
        """
        within_buffer = current_state.within_buffer(target_state, self.buffer_meters)
        logger.info(f"Goal test: {current_state} within {self.buffer_meters}m of {target_state}: {within_buffer}")
        return within_buffer

    def publish_route_to_feature_layer(self, routing_decision: RoutingDecision, layer_name: str = "Mock_Route") -> Optional[str]:
        """
        Mock publishing - just log the action
        """
        logger.info(f"Mock publishing route to feature layer: {layer_name}")
        logger.info(f"Route geometry: {routing_decision.route_geometry}")
        
        # Return a mock URL
        mock_url = f"https://mock.arcgis.com/layers/{layer_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        logger.info(f"Mock feature layer URL: {mock_url}")
        return mock_url

    def solve_routing_problem(self, 
                            start_address: str = "Bonn, Germany",
                            end_address: str = "Remagen, Germany") -> RoutingDecision:
        """
        Mock implementation of the complete routing problem solution
        """
        logger.info(f"Mock solving routing problem: {start_address} → {end_address}")
        
        try:
            # Step 1: Define Initial State
            start_state = self.geocode_location(start_address)
            logger.info(f"Mock initial state: {start_state}")
            
            # Step 2: Define Goal State
            goal_state = self.geocode_location(end_address)
            logger.info(f"Mock goal state: {goal_state}")
            
            # Step 3: Apply Transition Model
            routing_decision = self.compute_route(start_state, goal_state)
            
            # Step 4: Goal Test  
            # Note: goal_reached means we successfully computed a route to destination
            # The buffer test checks if start == end (already at destination)
            goal_test_result = self.goal_test(routing_decision.current_state, routing_decision.target_state)
            logger.info(f"Buffer-based goal test (are we already there?): {goal_test_result}")
            # Keep goal_reached as True since we computed a route to destination
            
            # Step 5: Mock publishing
            feature_layer_url = self.publish_route_to_feature_layer(routing_decision)
            if feature_layer_url:
                logger.info(f"Mock route published to: {feature_layer_url}")
            
            logger.info(f"Mock routing problem solved: {routing_decision.summary()}")
            return routing_decision
            
        except Exception as e:
            logger.error(f"Error in mock routing problem: {e}")
            raise

    def validate_decision(self, routing_decision: RoutingDecision) -> bool:
        """
        Validate routing decision (same as real agent)
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
        
        logger.info("Mock routing decision validated successfully")
        return True
    
    def _is_valid_coordinate(self, location: LocationState) -> bool:
        """Check if location has valid coordinates"""
        return (-90 <= location.latitude <= 90 and 
                -180 <= location.longitude <= 180)


# Demo function
def demo_mock_routing():
    """Demonstrate the mock routing agent functionality"""
    print("🧪 Mock Routing Agent Demo")
    print("=" * 40)
    
    # Initialize mock agent
    agent = MockRoutingAgent()
    
    # Solve the Bonn to Remagen problem
    result = agent.solve_routing_problem()
    
    print(f"\n📊 MOCK ROUTING RESULTS")
    print("=" * 30)
    print(f"Route: {result.summary()}")
    print(f"Start: {result.current_state}")
    print(f"Goal: {result.target_state}")
    print(f"Distance: {result.total_distance:.2f} km")
    print(f"Travel Time: {result.total_travel_time:.2f} minutes")
    print(f"Multi-criteria Cost: {result.get_multi_criteria_cost():.2f}")
    print(f"Confidence: {result.confidence:.2f}")
    
    # Validate the result
    is_valid = agent.validate_decision(result)
    print(f"Validation: {'✅ PASSED' if is_valid else '❌ FAILED'}")
    
    return result


if __name__ == "__main__":
    demo_mock_routing()