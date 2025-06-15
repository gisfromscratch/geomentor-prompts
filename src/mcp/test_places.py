#!/usr/bin/env python3
"""
Test script for nearby places search functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'server', 'location'))

from location_server import search_nearby_places, find_places, find_places_by_coordinates, generate_places_map_html

def test_places_functions_structure():
    """Test that places search functions are properly structured"""
    print("Testing places functions structure...")
    
    # Test that functions exist and are callable
    assert callable(search_nearby_places), "search_nearby_places should be callable"
    assert callable(find_places), "find_places should be callable"
    assert callable(find_places_by_coordinates), "find_places_by_coordinates should be callable"
    assert callable(generate_places_map_html), "generate_places_map_html should be callable"
    
    print("✓ All places functions are properly structured")

def test_search_nearby_places_structure():
    """Test that search_nearby_places function structure is correct"""
    print("Testing search_nearby_places structure...")
    
    # Test with known coordinates (Google headquarters)
    test_lat = 37.4219999
    test_lon = -122.0840575
    
    result = search_nearby_places(test_lat, test_lon)
    assert "success" in result, "Result should have success field"
    assert "search_location" in result, "Result should have search_location field"
    assert "places" in result, "Result should have places field"
    assert "total_results" in result, "Result should have total_results field"
    
    # Check search location is preserved
    assert result["search_location"]["latitude"] == test_lat, "Latitude should be preserved"
    assert result["search_location"]["longitude"] == test_lon, "Longitude should be preserved"
    
    # Either success with places or failure with error
    if result["success"]:
        assert isinstance(result["places"], list), "Places should be a list when successful"
        assert result["total_results"] >= 0, "Total results should be non-negative"
        
        # If places found, check structure
        if result["places"]:
            place = result["places"][0]
            assert "name" in place, "Place should have name"
            assert "coordinates" in place, "Place should have coordinates"
            assert "address" in place, "Place should have address"
    else:
        assert "error" in result, "Should have error message when unsuccessful"
    
    print("✓ search_nearby_places structure working correctly")

def test_find_places_structure():
    """Test that find_places function structure is correct"""
    print("Testing find_places structure...")
    
    # Test with a simple location string
    test_location = "San Francisco, CA"
    
    result = find_places(test_location)
    assert "success" in result, "Result should have success field"
    
    # Either success with search results or failure with error
    if result["success"]:
        assert "search_query" in result, "Should have search_query when successful"
        assert "results" in result, "Should have results when successful"
        assert "map_visualization" in result, "Should have map_visualization when successful"
        assert "chat_summary" in result, "Should have chat_summary when successful"
        
        # Check search query structure
        search_query = result["search_query"]
        assert "location" in search_query, "Search query should have location"
        assert "coordinates" in search_query, "Search query should have coordinates"
        assert "radius_meters" in search_query, "Search query should have radius_meters"
        
        # Check results structure
        results = result["results"]
        assert "total_found" in results, "Results should have total_found"
        assert "places" in results, "Results should have places"
        assert isinstance(results["places"], list), "Places should be a list"
    else:
        assert "error" in result, "Should have error message when unsuccessful"
    
    print("✓ find_places structure working correctly")

def test_find_places_by_coordinates_structure():
    """Test that find_places_by_coordinates function structure is correct"""
    print("Testing find_places_by_coordinates structure...")
    
    # Test with known coordinates
    test_lat = 37.7749
    test_lon = -122.4194
    
    result = find_places_by_coordinates(test_lat, test_lon)
    assert "success" in result, "Result should have success field"
    
    # Either success with search results or failure with error
    if result["success"]:
        assert "search_query" in result, "Should have search_query when successful"
        assert "results" in result, "Should have results when successful"
        assert "map_visualization" in result, "Should have map_visualization when successful"
        assert "chat_summary" in result, "Should have chat_summary when successful"
        
        # Check search query structure
        search_query = result["search_query"]
        assert "coordinates" in search_query, "Search query should have coordinates"
        assert search_query["coordinates"]["latitude"] == test_lat, "Latitude should be preserved"
        assert search_query["coordinates"]["longitude"] == test_lon, "Longitude should be preserved"
    else:
        assert "error" in result, "Should have error message when unsuccessful"
    
    print("✓ find_places_by_coordinates structure working correctly")

def test_parameter_validation():
    """Test parameter validation in places functions"""
    print("Testing parameter validation...")
    
    # Test radius clamping
    result = find_places_by_coordinates(37.7749, -122.4194, radius=100000)  # Over max
    if result["success"]:
        assert result["search_query"]["radius_meters"] <= 50000, "Radius should be clamped to max"
    
    result = find_places_by_coordinates(37.7749, -122.4194, radius=5)  # Under min
    if result["success"]:
        assert result["search_query"]["radius_meters"] >= 10, "Radius should be clamped to min"
    
    # Test max_results clamping
    result = find_places_by_coordinates(37.7749, -122.4194, max_results=100)  # Over max
    if result["success"]:
        assert result["search_query"]["max_results"] <= 50, "Max results should be clamped to max"
    
    result = find_places_by_coordinates(37.7749, -122.4194, max_results=0)  # Under min
    if result["success"]:
        assert result["search_query"]["max_results"] >= 1, "Max results should be clamped to min"
    
    print("✓ Parameter validation working correctly")

def test_error_handling():
    """Test error handling in places functions"""
    print("Testing places error handling...")
    
    # Test with invalid location (should fail gracefully)
    result = find_places("")
    assert "success" in result, "Result should have success field"
    assert "error" in result or "results" in result, "Result should have error or results"
    
    # Test with extreme coordinates
    result = find_places_by_coordinates(999.0, 999.0)
    assert "success" in result, "Result should have success field"
    # Network call might fail, but function should handle gracefully
    
    print("✓ Places error handling working correctly")

def test_category_filtering():
    """Test category filtering functionality"""
    print("Testing category filtering...")
    
    # Test with category filter
    result = find_places_by_coordinates(37.7749, -122.4194, category="restaurant")
    assert "success" in result, "Result should have success field"
    
    if result["success"]:
        assert result["search_query"]["category_filter"] == "restaurant", "Category filter should be preserved"
    
    print("✓ Category filtering working correctly")

def test_map_html_generation():
    """Test places map HTML generation"""
    print("Testing places map HTML generation...")
    
    # Create test places data
    test_places = [
        {
            "name": "Test Place 1",
            "coordinates": {"latitude": 37.7749, "longitude": -122.4194},
            "address": "123 Test St, San Francisco, CA"
        },
        {
            "name": "Test Place 2", 
            "coordinates": {"latitude": 37.7750, "longitude": -122.4195},
            "address": "456 Test Ave, San Francisco, CA"
        }
    ]
    
    html = generate_places_map_html(37.7749, -122.4194, test_places, 1000, "San Francisco")
    
    assert isinstance(html, str), "HTML should be a string"
    assert len(html) > 0, "HTML should not be empty"
    assert "iframe" in html.lower(), "HTML should contain iframe"
    assert "san francisco" in html.lower(), "HTML should contain location name"
    assert "test place 1" in html.lower(), "HTML should contain place names"
    
    print("✓ Places map HTML generation working correctly")

def main():
    """Run all places tests"""
    print("Running nearby places search functionality tests...\n")
    
    try:
        test_places_functions_structure()
        test_search_nearby_places_structure()
        test_find_places_structure()
        test_find_places_by_coordinates_structure()
        test_parameter_validation()
        test_error_handling()
        test_category_filtering()
        test_map_html_generation()
        
        print("\n✅ All places tests passed! Nearby places search functionality is working correctly.")
        return 0
        
    except Exception as e:
        print(f"\n❌ Places test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())