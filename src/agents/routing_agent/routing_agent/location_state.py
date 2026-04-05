"""
Location State and Routing Decision Classes

This module defines the state representation and decision structures for the routing agent.
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Tuple, Dict, Any

logger = logging.getLogger(__name__)


@dataclass
class LocationState:
    """Represents a location state in the routing problem"""
    
    latitude: float
    longitude: float
    address: Optional[str] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def distance_to(self, other: 'LocationState') -> float:
        """
        Calculate approximate distance to another location state using Haversine formula
        Returns distance in meters
        """
        import math
        
        R = 6371000  # Earth's radius in meters
        
        lat1_rad = math.radians(self.latitude)
        lat2_rad = math.radians(other.latitude)
        delta_lat = math.radians(other.latitude - self.latitude)
        delta_lon = math.radians(other.longitude - self.longitude)
        
        a = (math.sin(delta_lat/2)**2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    def within_buffer(self, other: 'LocationState', buffer_meters: float) -> bool:
        """Check if this location is within buffer distance of another location"""
        distance = self.distance_to(other)
        return distance <= buffer_meters
    
    def __str__(self):
        return f"LocationState({self.latitude:.6f}, {self.longitude:.6f})"
    
    def __repr__(self):
        return self.__str__()


@dataclass
class RouteSegment:
    """Represents a segment in a route with cost information"""
    
    start_location: LocationState
    end_location: LocationState
    travel_time_minutes: float
    distance_km: float
    instructions: Optional[str] = None
    geometry: Optional[Dict[str, Any]] = None  # Store route geometry
    
    @property
    def cost(self) -> float:
        """Primary cost metric (travel time in minutes)"""
        return self.travel_time_minutes


@dataclass
class RoutingDecision:
    """Decision output from the routing agent"""
    
    route_segments: List[RouteSegment]
    total_travel_time: float  # minutes
    total_distance: float  # km
    goal_reached: bool
    current_state: LocationState
    target_state: LocationState
    confidence: float  # 0-1 confidence in the route
    timestamp: datetime
    route_geometry: Optional[Dict[str, Any]] = None  # Full route polyline
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    @property
    def path_cost(self) -> float:
        """Total path cost (primary metric: travel time)"""
        return self.total_travel_time
    
    def get_multi_criteria_cost(self, time_weight: float = 0.7, distance_weight: float = 0.3) -> float:
        """
        Calculate multi-criteria cost combining time and distance
        Can be extended for risk factors later
        """
        # Normalize time (minutes) and distance (km) to similar scales
        normalized_time = self.total_travel_time / 60  # Convert to hours for comparison
        normalized_distance = self.total_distance
        
        return (time_weight * normalized_time + distance_weight * normalized_distance)
    
    def summary(self) -> str:
        """Return a summary string of the routing decision"""
        status = "✅ Goal reached" if self.goal_reached else "❌ Goal not reached"
        return (f"{status} - {len(self.route_segments)} segments, "
                f"{self.total_travel_time:.1f} min, {self.total_distance:.2f} km "
                f"(confidence: {self.confidence:.2f})")