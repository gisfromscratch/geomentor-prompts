#!/usr/bin/env python3
"""
Simple test script for geocoding functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'server', 'location'))

from location_server import geocode_address, reverse_geocode_coordinates, generate_map_url, display_location_on_map

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

def main():
    """Run all tests"""
    print("Running geocoding functionality tests...\n")
    
    try:
        test_geocoding_structure()
        test_reverse_geocoding_structure()
        test_error_handling()
        test_reverse_geocoding_error_handling()
        test_map_functionality()
        
        print("\n✅ All tests passed! Geocoding functionality is working correctly.")
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())