#!/usr/bin/env python3
"""
Simple test script for geocoding functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'server', 'location'))

from location_server import geocode_address, geocoded_metadata, get_geocoded_metadata, generate_map_url, display_location_on_map

def test_geocoding_structure():
    """Test that geocoding functions are properly structured"""
    print("Testing geocoding structure...")
    
    # Test that functions exist and are callable
    assert callable(geocode_address), "geocode_address should be callable"
    assert callable(get_geocoded_metadata), "get_geocoded_metadata should be callable"
    assert isinstance(geocoded_metadata, dict), "geocoded_metadata should be a dictionary"
    
    print("✓ All geocoding functions are properly structured")

def test_metadata_storage():
    """Test metadata storage functionality"""
    print("Testing metadata storage...")
    
    # Clear any existing metadata
    geocoded_metadata.clear()
    
    # Simulate storing geocoded result
    test_address = "123 Test Street, Test City"
    test_result = {
        "success": True,
        "address": test_address,
        "formatted_address": "123 Test St, Test City, TC 12345",
        "coordinates": {
            "latitude": 37.4419,
            "longitude": -122.1430
        },
        "score": 95,
        "attributes": {},
        "raw_response": {}
    }
    
    geocoded_metadata[test_address] = test_result
    
    # Test retrieval
    retrieved = get_geocoded_metadata(test_address)
    assert retrieved == test_result, "Retrieved metadata should match stored metadata"
    
    # Test getting all metadata
    all_metadata = get_geocoded_metadata()
    assert all_metadata["total_geocoded"] == 1, "Should have 1 geocoded address"
    assert test_address in all_metadata["addresses"], "Test address should be in address list"
    
    print("✓ Metadata storage and retrieval working correctly")

def test_error_handling():
    """Test error handling in geocoding"""
    print("Testing error handling...")
    
    # Test with empty address (this will likely fail due to network, but should handle gracefully)
    result = geocode_address("")
    assert "success" in result, "Result should have success field"
    assert "address" in result, "Result should have address field"
    assert "error" in result or "coordinates" in result, "Result should have error or coordinates"
    
    print("✓ Error handling working correctly")

def test_map_functionality():
    """Test map display functionality"""
    print("Testing map functionality...")
    
    # Set up test data
    test_address = "123 Test Street, Test City"
    test_result = {
        "success": True,
        "address": test_address,
        "formatted_address": "123 Test St, Test City, TC 12345",
        "coordinates": {
            "latitude": 37.4419,
            "longitude": -122.1430
        },
        "score": 95,
        "attributes": {},
        "raw_response": {}
    }
    
    geocoded_metadata[test_address] = test_result
    
    # Test map URL generation
    map_data = generate_map_url(test_address)
    assert map_data["success"] == True, "Map URL generation should succeed"
    assert "map_urls" in map_data, "Should contain map URLs"
    assert "google_maps" in map_data["map_urls"], "Should include Google Maps URL"
    assert "embed_html" in map_data, "Should include embed HTML"
    
    # Test complete map display
    display_data = display_location_on_map(test_address)
    assert display_data["success"] == True, "Map display should succeed"
    assert "coordinates" in display_data, "Should include coordinates"
    assert "embed_html" in display_data, "Should include embed HTML"
    assert "markdown_map" in display_data, "Should include markdown map"
    
    print("✓ Map functionality working correctly")

def main():
    """Run all tests"""
    print("Running geocoding functionality tests...\n")
    
    try:
        test_geocoding_structure()
        test_metadata_storage() 
        test_error_handling()
        test_map_functionality()
        
        print("\n✅ All tests passed! Geocoding functionality is working correctly.")
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())