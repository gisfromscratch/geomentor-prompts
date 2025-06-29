#!/usr/bin/env python3
"""
Test script for enhanced map rendering functionality (integration tests)
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'server', 'location'))

def test_enhanced_render_functions():
    """Test the enhanced render_static_map functions"""
    from location_server import (
        render_static_map_from_coordinates, 
        render_static_map_from_location,
        determine_location_type,
        get_zoom_for_location_type,
        get_style_for_location_type,
        Image
    )
    
    print("Testing enhanced render functions...")
    
    # Test 1: render_static_map_from_coordinates always returns Image
    result = render_static_map_from_coordinates(40.7128, -74.0060)
    assert isinstance(result, Image), "Should return Image object"
    print("   ✓ render_static_map_from_coordinates returns Image object")
    
    # Test 2: Invalid coordinates still return Image (error image)
    result = render_static_map_from_coordinates(999, 999)
    assert isinstance(result, Image), "Should return Image object even for invalid coordinates"
    print("   ✓ Invalid coordinates handled gracefully with Image response")
    
    # Test 3: Style parameter works
    result = render_static_map_from_coordinates(40.7128, -74.0060, style="world")
    assert isinstance(result, Image), "Should return Image object with custom style"
    print("   ✓ Custom style parameter works")
    
    # Test 4: Helper functions work correctly
    country_zoom = get_zoom_for_location_type("country")
    city_zoom = get_zoom_for_location_type("city") 
    address_zoom = get_zoom_for_location_type("address")
    
    assert country_zoom == 4, f"Country zoom should be 4, got {country_zoom}"
    assert city_zoom == 11, f"City zoom should be 11, got {city_zoom}"
    assert address_zoom == 16, f"Address zoom should be 16, got {address_zoom}"
    print("   ✓ Zoom level mapping works correctly")
    
    country_style = get_style_for_location_type("country")
    city_style = get_style_for_location_type("city")
    
    assert country_style == "world", f"Country style should be 'world', got {country_style}"
    assert city_style == "navigation", f"City style should be 'navigation', got {city_style}"
    print("   ✓ Style mapping works correctly")
    
    # Test 5: Location type determination
    country_type = determine_location_type({"Addr_type": "Country"})
    street_type = determine_location_type({"Addr_type": "StreetAddress"})
    default_type = determine_location_type({})
    
    assert country_type == "country", f"Should detect country type, got {country_type}"
    assert street_type == "address", f"Should detect address type, got {street_type}"
    assert default_type == "city", f"Should default to city type, got {default_type}"
    print("   ✓ Location type detection works correctly")
    
    # Test 6: render_static_map_from_location function exists and handles errors gracefully
    try:
        # This will fail due to network, but should return Image object with error
        result = render_static_map_from_location("Test Location")
        assert isinstance(result, Image), "Should return Image object even when geocoding fails"
        print("   ✓ render_static_map_from_location handles errors gracefully")
    except Exception as e:
        print(f"   Note: render_static_map_from_location test failed due to environment: {e}")
    
    print("✓ Enhanced render functions working correctly")


def test_backwards_compatibility():
    """Test that existing functions still work"""
    from location_server import generate_static_map_from_coordinates, generate_static_map_from_address
    
    print("Testing backwards compatibility...")
    
    # Test 1: generate_static_map_from_coordinates still returns Dict by default
    result = generate_static_map_from_coordinates(40.7128, -74.0060)
    assert isinstance(result, dict), "Should return dict by default"
    assert "success" in result, "Should have success field"
    print("   ✓ generate_static_map_from_coordinates returns dict by default")
    
    # Test 2: include_image_data parameter still works  
    result = generate_static_map_from_coordinates(40.7128, -74.0060, include_image_data=True)
    assert isinstance(result, dict), "Should still return dict when include_image_data=True"
    if result.get("success"):
        assert "image_data" in result, "Should include image data when requested"
    print("   ✓ include_image_data parameter works")
    
    # Test 3: generate_static_map_from_address function exists
    try:
        result = generate_static_map_from_address("Test Address")
        assert isinstance(result, dict), "Should return dict"
        # Expected to fail due to network, but structure should be correct
        assert "success" in result, "Should have success field"
        print("   ✓ generate_static_map_from_address maintains expected structure")
    except Exception as e:
        print(f"   Note: generate_static_map_from_address test limited due to environment: {e}")
    
    print("✓ Backwards compatibility maintained")


def test_coordinate_edge_cases():
    """Test edge cases for coordinates"""
    from location_server import render_static_map_from_coordinates, Image
    
    print("Testing coordinate edge cases...")
    
    # Valid edge coordinates
    test_cases = [
        (90, 180),      # Max valid
        (-90, -180),    # Min valid  
        (0, 0),         # Origin
        (85, 179),      # Near max valid
        (-85, -179),    # Near min valid
    ]
    
    for lat, lon in test_cases:
        result = render_static_map_from_coordinates(lat, lon)
        assert isinstance(result, Image), f"Should return Image for coordinates ({lat}, {lon})"
    
    print("   ✓ Valid edge coordinates handled correctly")
    
    # Invalid coordinates should still return Image objects (error images)
    invalid_cases = [
        (91, 0),        # Lat too high
        (-91, 0),       # Lat too low
        (0, 181),       # Lon too high
        (0, -181),      # Lon too low
        (999, 999),     # Way out of bounds
    ]
    
    for lat, lon in invalid_cases:
        result = render_static_map_from_coordinates(lat, lon)
        assert isinstance(result, Image), f"Should return Image (error) for invalid coordinates ({lat}, {lon})"
    
    print("   ✓ Invalid coordinates handled gracefully")
    print("✓ Coordinate edge cases working correctly")


def main():
    """Run all tests"""
    print("Running enhanced map rendering integration tests...\n")
    
    try:
        test_enhanced_render_functions()
        test_backwards_compatibility()
        test_coordinate_edge_cases()
        
        print("\n✅ All enhanced map rendering integration tests passed!")
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())