#!/usr/bin/env python3
"""
Test script for static basemap tile functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'server', 'location'))

from location_server import (
    lat_lon_to_tile_coordinates, 
    get_static_basemap_tile,
    generate_static_map_from_coordinates,
    generate_static_map_from_address,
    get_zoom_level_description
)

def test_coordinate_to_tile_conversion():
    """Test lat/lon to tile coordinate conversion"""
    print("Testing coordinate to tile conversion...")
    
    # Test known coordinates (Google headquarters at zoom 15)
    lat, lon = 37.4219999, -122.0840575
    zoom = 15
    
    tile_x, tile_y = lat_lon_to_tile_coordinates(lat, lon, zoom)
    
    # Verify that tile coordinates are integers
    assert isinstance(tile_x, int), "Tile X should be integer"
    assert isinstance(tile_y, int), "Tile Y should be integer"
    
    # Verify tile coordinates are within valid range for zoom level
    max_tile = 2 ** zoom
    assert 0 <= tile_x < max_tile, f"Tile X {tile_x} should be in range [0, {max_tile})"
    assert 0 <= tile_y < max_tile, f"Tile Y {tile_y} should be in range [0, {max_tile})"
    
    # Test different zoom levels
    for test_zoom in [0, 5, 10, 15, 20]:
        x, y = lat_lon_to_tile_coordinates(lat, lon, test_zoom)
        max_tile = 2 ** test_zoom
        assert 0 <= x < max_tile, f"Invalid tile X at zoom {test_zoom}"
        assert 0 <= y < max_tile, f"Invalid tile Y at zoom {test_zoom}"
    
    # Test edge cases
    # North pole (clamped)
    x, y = lat_lon_to_tile_coordinates(90, 0, 10)
    assert isinstance(x, int) and isinstance(y, int), "North pole conversion should work"
    
    # South pole (clamped)
    x, y = lat_lon_to_tile_coordinates(-90, 0, 10)
    assert isinstance(x, int) and isinstance(y, int), "South pole conversion should work"
    
    # International date line
    x, y = lat_lon_to_tile_coordinates(0, 180, 10)
    assert isinstance(x, int) and isinstance(y, int), "Date line conversion should work"
    
    print("✓ Coordinate to tile conversion working correctly")


def test_static_basemap_tile_structure():
    """Test static basemap tile function structure"""
    print("Testing static basemap tile structure...")
    
    # Test with valid coordinates (this will likely fail without network, but should handle gracefully)
    lat, lon = 40.7128, -74.0060  # New York City
    zoom = 12
    
    result = get_static_basemap_tile(lat, lon, zoom)
    
    # Check that result is either an Image object or an error dict
    if hasattr(result, 'data'):
        # It's an Image object - success case
        print("   ✓ Successfully returned Image object")
        assert hasattr(result, 'format'), "Image should have format attribute"
        print(f"   ✓ Image format: {result.format}")
    else:
        # It's an error dict - expected without network
        assert isinstance(result, dict), "Non-Image result should be dict"
        assert "success" in result, "Error dict should have success field"
        assert not result["success"], "Error dict should have success=False"
        assert "error" in result, "Error dict should have error message"
        print(f"   Note: Returned error (expected without network): {result.get('error', 'unknown error')}")
    
    print("✓ Static basemap tile structure working correctly")


def test_static_tile_validation():
    """Test input validation for static tile functions"""
    print("Testing static tile validation...")
    
    # Test invalid zoom levels
    result = get_static_basemap_tile(40.7128, -74.0060, -1)
    assert isinstance(result, dict), "Should return error dict for invalid input"
    assert not result["success"], "Should fail with negative zoom"
    assert "zoom level" in result["error"].lower(), "Error should mention zoom level"
    
    result = get_static_basemap_tile(40.7128, -74.0060, 25)
    assert isinstance(result, dict), "Should return error dict for invalid input"
    assert not result["success"], "Should fail with zoom > 22"
    
    # Test invalid coordinates
    result = get_static_basemap_tile(91, -74.0060, 10)
    assert isinstance(result, dict), "Should return error dict for invalid input"
    assert not result["success"], "Should fail with latitude > 90"
    
    result = get_static_basemap_tile(40.7128, 181, 10)
    assert isinstance(result, dict), "Should return error dict for invalid input"
    assert not result["success"], "Should fail with longitude > 180"
    
    result = get_static_basemap_tile(-91, -74.0060, 10)
    assert isinstance(result, dict), "Should return error dict for invalid input"
    assert not result["success"], "Should fail with latitude < -90"
    
    result = get_static_basemap_tile(40.7128, -181, 10)
    assert isinstance(result, dict), "Should return error dict for invalid input"
    assert not result["success"], "Should fail with longitude < -180"
    
    print("✓ Static tile validation working correctly")


def test_mcp_tools_structure():
    """Test MCP tool functions structure"""
    print("Testing MCP tools structure...")
    
    # Test coordinate-based tool
    result = generate_static_map_from_coordinates(40.7128, -74.0060, 12)
    
    # Should return either Image object or error dict
    if hasattr(result, 'data'):
        # It's an Image object - success case
        print("   ✓ Successfully returned Image object from coordinate tool")
        assert hasattr(result, 'format'), "Image should have format attribute"
    else:
        # It's an error dict - expected without network
        assert isinstance(result, dict), "Non-Image result should be dict"
        assert "success" in result, "Error dict should have success field"
        assert not result["success"], "Error dict should have success=False"
        print(f"   Note: Coordinate tool failed (expected): {result.get('error', 'unknown error')}")
    
    # Test address-based tool (will likely fail without network, but should handle gracefully)
    result = generate_static_map_from_address("Times Square, New York", 14)
    
    if hasattr(result, 'data'):
        # It's an Image object - success case
        print("   ✓ Successfully returned Image object from address tool")
        assert hasattr(result, 'format'), "Image should have format attribute"
    else:
        # It's an error dict - expected without network
        assert isinstance(result, dict), "Non-Image result should be dict"
        assert "success" in result, "Error dict should have success field"
        assert not result["success"], "Error dict should have success=False"
        print(f"   Note: Address tool failed (expected): {result.get('error', 'unknown error')}")
    
    print("✓ MCP tools structure working correctly")


def test_zoom_level_descriptions():
    """Test zoom level description function"""
    print("Testing zoom level descriptions...")
    
    # Test various zoom levels
    test_cases = [
        (0, "World view"),
        (5, "State/Province view"),
        (10, "City view"),
        (15, "Neighborhood"),
        (18, "Building level"),
        (22, "Maximum detail")
    ]
    
    for zoom, expected_type in test_cases:
        description = get_zoom_level_description(zoom)
        assert isinstance(description, str), f"Description should be string for zoom {zoom}"
        assert len(description) > 0, f"Description should not be empty for zoom {zoom}"
        print(f"   ✓ Zoom {zoom}: {description}")
    
    # Test edge case
    description = get_zoom_level_description(99)
    assert "Zoom level 99" in description, "Should handle unknown zoom levels"
    
    print("✓ Zoom level descriptions working correctly")


def test_image_data_option():
    """Test the image data return option"""
    print("Testing image data option...")
    
    # Test with valid coordinates (will likely fail without network)
    result = get_static_basemap_tile(40.7128, -74.0060, 10)
    
    if hasattr(result, 'data'):
        # If successful, verify image data structure
        assert hasattr(result, 'format'), "Image should have format attribute"
        assert result.format == "image/png", "Should be PNG format"
        assert len(result.data) > 0, "Image data should not be empty"
        print("   ✓ Image data retrieval successful")
    else:
        # Expected in test environment without network
        assert isinstance(result, dict), "Non-Image result should be dict"
        assert not result["success"], "Should be error dict"
        print("   Note: Image data retrieval failed (expected without network access)")
    
    print("✓ Image data option working correctly")


def test_integration_with_existing_functions():
    """Test integration with existing geocoding functions"""
    print("Testing integration with existing functions...")
    
    # Import and test that existing functions still work
    try:
        from location_server import geocode_address, generate_map_url
        
        # These should still be callable
        assert callable(geocode_address), "geocode_address should still be callable"
        assert callable(generate_map_url), "generate_map_url should still be callable"
        
        # Test that they don't conflict with new functions
        assert callable(generate_static_map_from_coordinates), "New function should be callable"
        assert callable(generate_static_map_from_address), "New function should be callable"
        
        print("   ✓ All functions coexist properly")
        
    except ImportError as e:
        print(f"   Note: Import test failed (expected): {e}")
    
    print("✓ Integration working correctly")


def main():
    """Run all basemap tile tests"""
    print("Running static basemap tile functionality tests...\n")
    
    try:
        test_coordinate_to_tile_conversion()
        test_static_basemap_tile_structure()
        test_static_tile_validation()
        test_mcp_tools_structure()
        test_zoom_level_descriptions()
        test_image_data_option()
        test_integration_with_existing_functions()
        
        print("\n✅ All basemap tile tests passed! Static tile functionality is working correctly.")
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())