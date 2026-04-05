"""
Unit tests for the Routing Agent

These tests validate the core functionality of the routing agent
using mocked ArcGIS services where appropriate.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import sys
import os

# Add parent directories to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from routing_agent.location_state import LocationState, RouteSegment, RoutingDecision


class TestLocationState(unittest.TestCase):
    """Test cases for LocationState class"""
    
    def setUp(self):
        self.bonn = LocationState(50.7374, 7.0982, "Bonn")
        self.remagen = LocationState(50.5791, 7.2281, "Remagen") 
    
    def test_location_creation(self):
        """Test basic location state creation"""
        location = LocationState(50.0, 7.0, "Test Location")
        
        self.assertEqual(location.latitude, 50.0)
        self.assertEqual(location.longitude, 7.0)
        self.assertEqual(location.address, "Test Location")
        self.assertIsNotNone(location.timestamp)
    
    def test_distance_calculation(self):
        """Test distance calculation between locations"""
        distance = self.bonn.distance_to(self.remagen)
        
        # Expected distance Bonn to Remagen is approximately 15-20 km
        self.assertGreater(distance, 10000)  # At least 10km 
        self.assertLess(distance, 30000)     # At most 30km
    
    def test_within_buffer(self):
        """Test buffer distance checking"""
        # Same location should be within any buffer
        self.assertTrue(self.bonn.within_buffer(self.bonn, 100))
        
        # Bonn to Remagen should not be within 200m buffer
        self.assertFalse(self.bonn.within_buffer(self.remagen, 200))
        
        # But should be within 50km buffer
        self.assertTrue(self.bonn.within_buffer(self.remagen, 50000))


class TestRouteSegment(unittest.TestCase):
    """Test cases for RouteSegment class"""
    
    def setUp(self):
        self.start = LocationState(50.0, 7.0, "Start")
        self.end = LocationState(50.1, 7.1, "End")
    
    def test_segment_creation(self):
        """Test route segment creation"""
        segment = RouteSegment(
            start_location=self.start,
            end_location=self.end,
            travel_time_minutes=10.5,
            distance_km=5.2,
            instructions="Drive straight"
        )
        
        self.assertEqual(segment.cost, 10.5)  # Cost should be travel time
        self.assertEqual(segment.travel_time_minutes, 10.5)
        self.assertEqual(segment.distance_km, 5.2)
        self.assertEqual(segment.instructions, "Drive straight")


class TestRoutingDecision(unittest.TestCase):
    """Test cases for RoutingDecision class"""
    
    def setUp(self):
        self.start = LocationState(50.0, 7.0, "Start")
        self.end = LocationState(50.1, 7.1, "End")
        self.segment = RouteSegment(
            self.start, self.end, 15.0, 8.5, "Test segment"
        )
    
    def test_decision_creation(self):
        """Test routing decision creation"""
        decision = RoutingDecision(
            route_segments=[self.segment],
            total_travel_time=15.0,
            total_distance=8.5,
            goal_reached=True,
            current_state=self.start,
            target_state=self.end,
            confidence=0.9,
            timestamp=datetime.now()
        )
        
        self.assertEqual(decision.path_cost, 15.0)
        self.assertTrue(decision.goal_reached)
        self.assertEqual(decision.confidence, 0.9)
        self.assertEqual(len(decision.route_segments), 1)
    
    def test_multi_criteria_cost(self):
        """Test multi-criteria cost calculation"""
        decision = RoutingDecision(
            route_segments=[self.segment],
            total_travel_time=60.0,  # 1 hour
            total_distance=30.0,     # 30 km
            goal_reached=True,
            current_state=self.start,
            target_state=self.end,
            confidence=1.0,
            timestamp=datetime.now()
        )
        
        # Default weights: 0.7 time, 0.3 distance
        multi_cost = decision.get_multi_criteria_cost()
        expected_cost = 0.7 * 1.0 + 0.3 * 30.0  # 0.7 + 9.0 = 9.7
        self.assertAlmostEqual(multi_cost, expected_cost, places=1)
        
        # Test custom weights
        custom_cost = decision.get_multi_criteria_cost(time_weight=0.5, distance_weight=0.5)
        expected_custom = 0.5 * 1.0 + 0.5 * 30.0  # 0.5 + 15.0 = 15.5
        self.assertAlmostEqual(custom_cost, expected_custom, places=1)
    
    def test_summary(self):
        """Test decision summary string"""
        decision = RoutingDecision(
            route_segments=[self.segment],
            total_travel_time=15.0,
            total_distance=8.5,
            goal_reached=True,
            current_state=self.start,
            target_state=self.end,
            confidence=0.9,
            timestamp=datetime.now()
        )
        
        summary = decision.summary()
        self.assertIn("✅ Goal reached", summary)
        self.assertIn("15.0 min", summary)
        self.assertIn("8.5 km", summary)
        self.assertIn("0.90", summary)


class TestRoutingAgentCore(unittest.TestCase):
    """Test cases for core RoutingAgent functionality (without ArcGIS)"""
    
    def test_coordinate_validation(self):
        """Test coordinate validation method"""
        from routing_agent.agent import RoutingAgent
        agent = RoutingAgent.__new__(RoutingAgent)  # Create without __init__
        
        # Valid coordinates
        valid_location = LocationState(50.0, 7.0, "Valid")
        self.assertTrue(agent._is_valid_coordinate(valid_location))
        
        # Invalid latitude
        invalid_lat = LocationState(91.0, 7.0, "Invalid Lat")
        self.assertFalse(agent._is_valid_coordinate(invalid_lat))
        
        # Invalid longitude  
        invalid_lon = LocationState(50.0, 181.0, "Invalid Lon")
        self.assertFalse(agent._is_valid_coordinate(invalid_lon))


if __name__ == '__main__':
    unittest.main()