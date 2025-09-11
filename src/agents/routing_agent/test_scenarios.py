#!/usr/bin/env python3
"""
Test scenarios for the Routing Agent

This script runs various test scenarios to validate the routing agent
functionality and different problem formulations. Uses mock agent when
ArcGIS is not available.
"""

import sys
import os
from datetime import datetime

# Add the routing_agent package to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from routing_agent import RoutingAgent
    AGENT_TYPE = "ArcGIS"
except ImportError:
    from routing_agent import MockRoutingAgent as RoutingAgent
    AGENT_TYPE = "Mock"

from routing_agent import LocationState


def test_basic_routing():
    """Test basic Bonn to Remagen routing"""
    print(f"🧪 Test 1: Basic Bonn to Remagen Routing ({AGENT_TYPE})")
    print("-" * 50)
    
    agent = RoutingAgent()
    result = agent.solve_routing_problem()
    
    assert result is not None, "Routing result should not be None"
    assert result.total_travel_time > 0, "Travel time should be positive"
    assert result.total_distance > 0, "Distance should be positive"
    assert result.route_segments, "Route should have segments"
    
    print(f"✅ Basic routing test passed: {result.summary()}")
    return result


def test_geocoding_accuracy():
    """Test geocoding accuracy for German cities"""
    print(f"\n🧪 Test 2: Geocoding Accuracy ({AGENT_TYPE})")
    print("-" * 40)
    
    agent = RoutingAgent()
    
    # Test Bonn geocoding
    bonn = agent.geocode_location("Bonn, Germany")
    print(f"Bonn: {bonn}")
    
    # Validate Bonn coordinates (approximately)
    assert 50.7 < bonn.latitude < 50.8, f"Bonn latitude out of range: {bonn.latitude}"
    assert 7.0 < bonn.longitude < 7.2, f"Bonn longitude out of range: {bonn.longitude}"
    
    # Test Remagen geocoding  
    remagen = agent.geocode_location("Remagen, Germany")
    print(f"Remagen: {remagen}")
    
    # Validate Remagen coordinates (approximately)
    assert 50.5 < remagen.latitude < 50.7, f"Remagen latitude out of range: {remagen.latitude}"
    assert 7.1 < remagen.longitude < 7.3, f"Remagen longitude out of range: {remagen.longitude}"
    
    print("✅ Geocoding accuracy test passed")
    return bonn, remagen


def test_goal_test_functionality():
    """Test goal test with various buffer distances"""
    print("\n🧪 Test 3: Goal Test Functionality")
    print("-" * 40)
    
    agent = RoutingAgent()
    
    # Create test locations
    bonn = LocationState(50.7374, 7.0982, "Bonn")
    remagen = LocationState(50.5791, 7.2281, "Remagen")
    
    # Test goal test with different buffers
    buffer_200m = agent.goal_test(bonn, remagen)  # Should be False
    print(f"Goal test with 200m buffer: {buffer_200m}")
    
    # Test with same location (should be True)
    same_location = agent.goal_test(bonn, bonn)
    print(f"Goal test with same location: {same_location}")
    
    assert not buffer_200m, "Bonn and Remagen should not be within 200m"
    assert same_location, "Same location should pass goal test"
    
    print("✅ Goal test functionality passed")


def test_path_cost_calculation():
    """Test path cost and multi-criteria cost calculations"""
    print("\n🧪 Test 4: Path Cost Calculations")
    print("-" * 40)
    
    agent = RoutingAgent()
    result = agent.solve_routing_problem()
    
    # Test primary cost (travel time)
    primary_cost = result.path_cost
    print(f"Primary cost (travel time): {primary_cost:.2f} minutes")
    
    # Test multi-criteria cost
    multi_cost = result.get_multi_criteria_cost()
    print(f"Multi-criteria cost: {multi_cost:.2f}")
    
    # Test with different weights
    time_heavy = result.get_multi_criteria_cost(time_weight=0.9, distance_weight=0.1)
    distance_heavy = result.get_multi_criteria_cost(time_weight=0.3, distance_weight=0.7)
    
    print(f"Time-heavy cost: {time_heavy:.2f}")
    print(f"Distance-heavy cost: {distance_heavy:.2f}")
    
    assert primary_cost > 0, "Primary cost should be positive"
    assert multi_cost > 0, "Multi-criteria cost should be positive"
    
    print("✅ Path cost calculation test passed")


def test_route_validation():
    """Test route validation functionality"""
    print("\n🧪 Test 5: Route Validation")
    print("-" * 35)
    
    agent = RoutingAgent()
    result = agent.solve_routing_problem()
    
    # Test validation of good result
    is_valid = agent.validate_decision(result)
    print(f"Valid route validation: {is_valid}")
    
    # Test validation of None result
    none_valid = agent.validate_decision(None)
    print(f"None result validation: {none_valid}")
    
    assert is_valid, "Valid route should pass validation"
    assert not none_valid, "None result should fail validation"
    
    print("✅ Route validation test passed")


def test_alternative_locations():
    """Test routing between alternative German locations"""
    print("\n🧪 Test 6: Alternative Location Routing")
    print("-" * 45)
    
    agent = RoutingAgent()
    
    # Test Köln to Düsseldorf (different route)
    result = agent.solve_routing_problem(
        start_address="Köln, Germany",
        end_address="Düsseldorf, Germany"
    )
    
    print(f"Köln → Düsseldorf: {result.summary()}")
    
    assert result.total_travel_time > 0, "Alternative route should have travel time"
    assert result.confidence > 0, "Alternative route should have confidence"
    
    print("✅ Alternative location routing test passed")
    return result


def run_all_tests():
    """Run all routing agent tests"""
    print("🚀 Running Routing Agent Test Suite")
    print("=" * 50)
    
    try:
        # Run tests
        basic_result = test_basic_routing()
        bonn, remagen = test_geocoding_accuracy() 
        test_goal_test_functionality()
        test_path_cost_calculation()
        test_route_validation()
        alternative_result = test_alternative_locations()
        
        print("\n📊 TEST SUMMARY")
        print("=" * 20)
        print("✅ All tests passed successfully!")
        print(f"Primary test result: {basic_result.summary()}")
        print(f"Alternative test result: {alternative_result.summary()}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print(f"Test execution time: {datetime.now()}")
    print()
    
    success = run_all_tests()
    
    if success:
        print(f"\n🎉 All tests completed successfully!")
        sys.exit(0)
    else:
        print(f"\n💥 Tests failed")
        sys.exit(1)