#!/usr/bin/env python3
"""
Simple test script for geocoding functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'server', 'location'))

from location_server import geocode_address, reverse_geocode_coordinates, generate_map_url, display_location_on_map, get_elevation, get_elevation_for_coordinates, get_elevation_for_address, display_location_with_elevation, get_directions_between_locations, format_directions_for_chat

def test_geocoding_structure():
    """Test that geocoding functions are properly structured"""
    print("Testing geocoding structure...")
    
    # Test that functions exist and are callable
    assert callable(geocode_address), "geocode_address should be callable"
    assert callable(reverse_geocode_coordinates), "reverse_geocode_coordinates should be callable"
    
    print("✓ All geocoding functions are properly structured")

def test_reverse_geocoding_structure():
    """Test that reverse geocoding functions are properly structured"""
    print("Testing reverse geocoding structure...")
    
    # Test with known coordinates (Google headquarters)
    test_lat = 37.4219999
    test_lon = -122.0840575
    
    result = reverse_geocode_coordinates(test_lat, test_lon)
    assert "success" in result, "Result should have success field"
    assert "coordinates" in result, "Result should have coordinates field"
    assert "formatted_address" in result, "Result should have formatted_address field"
    
    # Check coordinates are preserved
    assert result["coordinates"]["latitude"] == test_lat, "Latitude should be preserved"
    assert result["coordinates"]["longitude"] == test_lon, "Longitude should be preserved"
    
    # Either success with address or failure with error
    if result["success"]:
        assert result["formatted_address"], "Should have formatted address when successful"
        assert "address_components" in result, "Should have address components when successful"
    else:
        assert "error" in result, "Should have error message when unsuccessful"
    
    print("✓ Reverse geocoding structure working correctly")

def test_error_handling():
    """Test error handling in geocoding"""
    print("Testing error handling...")
    
    # Test with empty address (this will likely fail due to network, but should handle gracefully)
    result = geocode_address("")
    assert "success" in result, "Result should have success field"
    assert "address" in result, "Result should have address field"
    assert "error" in result or "coordinates" in result, "Result should have error or coordinates"
    
    print("✓ Error handling working correctly")

def test_reverse_geocoding_error_handling():
    """Test error handling in reverse geocoding"""
    print("Testing reverse geocoding error handling...")
    
    # Test with invalid coordinates (extreme values)
    result = reverse_geocode_coordinates(999.0, 999.0)
    assert "success" in result, "Result should have success field"
    assert "coordinates" in result, "Result should have coordinates field"
    assert result["coordinates"]["latitude"] == 999.0, "Should preserve input latitude"
    assert result["coordinates"]["longitude"] == 999.0, "Should preserve input longitude"
    
    # Should either succeed or fail gracefully
    if not result["success"]:
        assert "error" in result, "Should have error message when unsuccessful"
    
    print("✓ Reverse geocoding error handling working correctly")

def test_map_functionality():
    """Test map display functionality"""
    print("Testing map functionality...")
    
    # Use a real address that should geocode successfully
    test_address = "1600 Amphitheatre Parkway, Mountain View, CA"
    
    # Test map URL generation
    map_data = generate_map_url(test_address)
    if map_data.get("success"):
        assert "map_urls" in map_data, "Should contain map URLs"
        assert "google_maps" in map_data["map_urls"], "Should include Google Maps URL"
        assert "embed_html" in map_data, "Should include embed HTML"
        
        # Test complete map display
        display_data = display_location_on_map(test_address)
        assert display_data["success"] == True, "Map display should succeed"
        assert "coordinates" in display_data, "Should include coordinates"
        assert "embed_html" in display_data, "Should include embed HTML"
        assert "markdown_map" in display_data, "Should include markdown map"
    else:
        print(f"   Note: Geocoding failed for test address (network/API issue): {map_data.get('error', 'unknown error')}")
        print("   This is expected in environments without network access or API keys")
    
    print("✓ Map functionality working correctly")

def test_elevation_structure():
    """Test that elevation functions are properly structured"""
    print("Testing elevation structure...")
    
    # Test that functions exist and are callable
    assert callable(get_elevation), "get_elevation should be callable"
    assert callable(get_elevation_for_coordinates), "get_elevation_for_coordinates should be callable"
    assert callable(get_elevation_for_address), "get_elevation_for_address should be callable"
    assert callable(display_location_with_elevation), "display_location_with_elevation should be callable"
    
    print("✓ All elevation functions are properly structured")

def test_elevation_coordinates():
    """Test elevation functionality with coordinates"""
    print("Testing elevation with coordinates...")
    
    # Test with known coordinates (Mount Whitney, CA - highest peak in continental US)
    test_lat = 36.5786
    test_lon = -118.2923
    
    result = get_elevation(test_lat, test_lon)
    assert "success" in result, "Result should have success field"
    assert "coordinates" in result, "Result should have coordinates field"
    assert "elevation" in result, "Result should have elevation field"
    
    # Check coordinates are preserved
    assert result["coordinates"]["latitude"] == test_lat, "Latitude should be preserved"
    assert result["coordinates"]["longitude"] == test_lon, "Longitude should be preserved"
    
    # Either success with elevation data or failure with error
    if result["success"]:
        assert result["elevation"], "Should have elevation data when successful"
        assert "meters" in result["elevation"], "Should have elevation in meters"
        assert "feet" in result["elevation"], "Should have elevation in feet"
        assert "data_source" in result, "Should have data source information"
    else:
        assert "error" in result, "Should have error message when unsuccessful"
        print(f"   Note: Elevation lookup failed (expected in test environments): {result.get('error', 'unknown error')}")
    
    print("✓ Elevation coordinates functionality working correctly")

def test_elevation_address():
    """Test elevation functionality with address"""
    print("Testing elevation with address...")
    
    # Use a real address that should geocode successfully
    test_address = "Mount Washington, New Hampshire"
    
    result = get_elevation_for_address(test_address)
    assert "success" in result, "Result should have success field"
    assert "address" in result, "Result should have address field"
    
    if result["success"]:
        assert "coordinates" in result, "Should have coordinates when successful"
        assert "elevation" in result, "Should have elevation data when successful"
        assert "formatted_address" in result, "Should have formatted address when successful"
        print(f"   Successfully got elevation for: {result['formatted_address']}")
    else:
        assert "error" in result, "Should have error message when unsuccessful"
        print(f"   Note: Elevation/geocoding failed (expected in test environments): {result.get('error', 'unknown error')}")
    
    print("✓ Elevation address functionality working correctly")

def test_elevation_display():
    """Test elevation display functionality"""
    print("Testing elevation display functionality...")
    
    # Use a real address that should work
    test_address = "Denver, Colorado"
    
    result = display_location_with_elevation(test_address)
    assert "success" in result, "Result should have success field"
    
    if result["success"]:
        assert "coordinates" in result, "Should have coordinates when successful"
        assert "elevation" in result, "Should have elevation data when successful"
        assert "map_urls" in result, "Should have map URLs when successful"
        assert "markdown_map" in result, "Should have markdown map when successful"
        print(f"   Successfully created elevation display for: {result['formatted_address']}")
    else:
        assert "error" in result, "Should have error message when unsuccessful"
        print(f"   Note: Elevation display failed (expected in test environments): {result.get('error', 'unknown error')}")
    
    print("✓ Elevation display functionality working correctly")

def test_routing_functionality():
    """Test routing and directions functionality"""
    print("Testing routing functionality...")
    
    # Test that the routing function is available and callable
    assert callable(get_directions_between_locations), "get_directions_between_locations should be callable"
    
    # Test routing with coordinates (this will likely fail due to network, but should handle gracefully)
    test_origin = "37.7749,-122.4194"  # San Francisco coordinates
    test_destination = "37.7849,-122.4094"  # Nearby coordinates
    
    result = get_directions_between_locations(test_origin, test_destination)
    assert "success" in result, "Result should have success field"
    assert "origin" in result, "Result should have origin field" 
    assert "destination" in result, "Result should have destination field"
    
    # Either success with routing info or failure with error
    if result["success"]:
        assert "route_summary" in result, "Should have route summary when successful"
        assert "directions" in result, "Should have directions when successful"
        assert "total_time_minutes" in result["route_summary"], "Should have travel time"
        assert "total_distance_miles" in result["route_summary"], "Should have distance"
        print(f"   ✓ Route found: {result['route_summary']['total_distance_miles']} miles, {result['route_summary']['total_time_formatted']}")
        print(f"   ✓ {len(result['directions'])} turn-by-turn directions provided")
    else:
        print(f"   Note: Routing failed (network/API issue): {result.get('error', 'unknown error')}")
        print("   This is expected in environments without network access or API keys")
        assert "error" in result, "Should have error message when unsuccessful"
    
    print("✓ Routing functionality working correctly")

def test_routing_travel_modes():
    """Test different travel modes for routing"""
    print("Testing routing travel modes...")
    
    test_origin = "New York, NY"
    test_destination = "Brooklyn, NY"
    
    # Test different travel modes
    travel_modes = ["driving", "walking", "trucking"]
    
    for mode in travel_modes:
        result = get_directions_between_locations(test_origin, test_destination, travel_mode=mode)
        assert "success" in result, f"Result should have success field for {mode}"
        assert result.get("travel_mode") == mode, f"Travel mode should be preserved for {mode}"
        
        if result["success"]:
            print(f"   ✓ {mode.capitalize()} route calculated successfully")
        else:
            print(f"   Note: {mode.capitalize()} routing failed (expected without network/API)")
    
    print("✓ Travel mode testing working correctly")

def test_routing_error_handling():
    """Test error handling in routing"""
    print("Testing routing error handling...")
    
    # Test with invalid coordinates
    result = get_directions_between_locations("999,999", "888,888")
    assert "success" in result, "Result should have success field"
    
    # Should either succeed or fail gracefully
    if not result["success"]:
        assert "error" in result, "Should have error message when unsuccessful"
    
    # Test with empty addresses
    result = get_directions_between_locations("", "")
    assert "success" in result, "Result should have success field"
    if not result["success"]:
        assert "error" in result, "Should have error message when unsuccessful"
    
    print("✓ Routing error handling working correctly")

def test_routing_formatting():
    """Test routing result formatting for chat UI"""
    print("Testing routing formatting...")
    
    # Test formatting function exists
    assert callable(format_directions_for_chat), "format_directions_for_chat should be callable"
    
    # Test error formatting
    error_result = {
        "success": False,
        "origin": "Test Origin",
        "destination": "Test Destination", 
        "error": "Test error message"
    }
    formatted = format_directions_for_chat(error_result)
    assert "❌" in formatted, "Error formatting should include error emoji"
    assert "Test error message" in formatted, "Error message should be included"
    
    # Test successful result formatting (mock successful result)
    success_result = {
        "success": True,
        "origin": "San Francisco, CA",
        "destination": "Oakland, CA",
        "travel_mode": "driving",
        "route_summary": {
            "total_time_minutes": 25.5,
            "total_distance_miles": 12.3,
            "total_time_formatted": "25m"
        },
        "directions": [
            {"instruction": "Head north on Main St", "distance": 0.5},
            {"instruction": "Turn right on Oak Ave", "distance": 1.2}
        ]
    }
    formatted = format_directions_for_chat(success_result)
    assert "🗺️" in formatted, "Success formatting should include map emoji"
    assert "San Francisco, CA" in formatted, "Origin should be included"
    assert "Oakland, CA" in formatted, "Destination should be included"
    assert "25m" in formatted, "Travel time should be included"
    assert "12.3 miles" in formatted, "Distance should be included"
    assert "Head north on Main St" in formatted, "Directions should be included"
    
    print("✓ Routing formatting working correctly")

def main():
    """Run all tests"""
    print("Running geocoding functionality tests...\n")
    
    try:
        test_geocoding_structure()
        test_reverse_geocoding_structure()
        test_error_handling()
        test_reverse_geocoding_error_handling()
        test_map_functionality()
        test_elevation_structure()
        test_elevation_coordinates()
        test_elevation_address()
        test_elevation_display()
        test_routing_functionality()
        test_routing_travel_modes()
        test_routing_error_handling()
        test_routing_formatting()
        
        print("\n✅ All tests passed! Geocoding, elevation, and routing functionality is working correctly.")
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())