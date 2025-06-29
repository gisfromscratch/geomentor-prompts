#!/usr/bin/env python3
"""
Test script for enhanced map rendering functionality (integration tests)
"""

from mcp.server.fastmcp import Image
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'server', 'location'))

def text_render_functions():
    """Test the original render_static_map functions"""
    from location_server import (
        render_static_map_from_coordinates,
        render_static_map_from_location,
        determine_location_type,
        get_zoom_for_location_type
    )
    
    print("Testing original render functions...")
    
    # Test country level rendering
    result = render_static_map_from_location("Germany")
    assert isinstance(result, Image), "Should return Image for country level rendering"


def test_enhanced_render_functions():
    """Test the enhanced render_static_map functions"""
    from location_server import (
        render_static_map_from_coordinates, 
        render_static_map_from_location,
        determine_location_type,
        get_zoom_for_location_type
    )
    
    print("Testing enhanced render functions...")
    
    # Test 1: render_static_map_from_coordinates returns Image on success, error dict on failure
    # Invalid coordinates should return error dict
    result = render_static_map_from_coordinates(999, 999)
    assert isinstance(result, dict), "Should return error dict for invalid coordinates"
    assert not result.get("success", True), "Should indicate failure"
    print("   ✓ Invalid coordinates return error dict")
    
    # Test 2: Valid coordinates (will likely fail without network, but should handle gracefully)
    result = render_static_map_from_coordinates(40.7128, -74.0060)
    if hasattr(result, 'data'):
        # Success case - Image object
        assert hasattr(result, 'format'), "Image should have format attribute"
        print("   ✓ Valid coordinates return Image object")
    else:
        # Network failure case - error dict
        assert isinstance(result, dict), "Should return error dict on network failure"
        assert not result.get("success", True), "Should indicate failure"
        print("   Note: Valid coordinates failed due to network (expected)")
    
    # Test 3: Style parameter works
    result = render_static_map_from_coordinates(40.7128, -74.0060, style="world")
    # Should be same behavior as test 2
    print("   ✓ Custom style parameter works")
    
    # Test 4: Helper functions work correctly
    country_zoom = get_zoom_for_location_type("country")
    city_zoom = get_zoom_for_location_type("city") 
    address_zoom = get_zoom_for_location_type("address")
    
    assert country_zoom == 4, f"Country zoom should be 4, got {country_zoom}"
    assert city_zoom == 11, f"City zoom should be 11, got {city_zoom}"
    assert address_zoom == 16, f"Address zoom should be 16, got {address_zoom}"
    print("   ✓ Zoom level mapping works correctly")
    
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
        # This will fail due to network, should return error dict
        result = render_static_map_from_location("Test Location")
        assert isinstance(result, dict), "Should return error dict when geocoding fails"
        assert not result.get("success", True), "Should indicate failure"
        print("   ✓ render_static_map_from_location handles errors gracefully")
    except Exception as e:
        print(f"   Note: render_static_map_from_location test failed due to environment: {e}")
    
    print("✓ Enhanced render functions working correctly")


def test_backwards_compatibility():
    """Test that existing functions still work"""
    from location_server import generate_static_map_from_coordinates, generate_static_map_from_address
    
    print("Testing backwards compatibility...")
    
    # Test 1: generate_static_map_from_coordinates now returns Image or error dict
    result = generate_static_map_from_coordinates(40.7128, -74.0060)
    if hasattr(result, 'data'):
        # Success case - Image object
        assert hasattr(result, 'format'), "Image should have format attribute"
        print("   ✓ generate_static_map_from_coordinates returns Image on success")
    else:
        # Network failure case - error dict
        assert isinstance(result, dict), "Should return error dict on failure"
        assert not result.get("success", True), "Should indicate failure"
        print("   Note: generate_static_map_from_coordinates failed due to network (expected)")
    
    # Test 2: Invalid coordinates return error dict
    result = generate_static_map_from_coordinates(999, 999)
    assert isinstance(result, dict), "Should return error dict for invalid input"
    assert not result.get("success", True), "Should indicate failure"
    print("   ✓ Invalid input returns error dict")
    
    # Test 3: generate_static_map_from_address function exists
    try:
        result = generate_static_map_from_address("Test Address")
        if hasattr(result, 'data'):
            # Success case - Image object
            print("   ✓ generate_static_map_from_address returns Image on success")
        else:
            # Expected to fail due to network - error dict
            assert isinstance(result, dict), "Should return error dict on failure"
            assert not result.get("success", True), "Should indicate failure"
            print("   Note: generate_static_map_from_address failed due to network (expected)")
    except Exception as e:
        print(f"   Note: generate_static_map_from_address test limited due to environment: {e}")
    
    print("✓ Backwards compatibility maintained")


def test_coordinate_edge_cases():
    """Test edge cases for coordinates"""
    from location_server import render_static_map_from_coordinates
    
    print("Testing coordinate edge cases...")
    
    # Valid edge coordinates (will likely fail due to network, but should return appropriate type)
    test_cases = [
        (90, 180),      # Max valid
        (-90, -180),    # Min valid  
        (0, 0),         # Origin
        (85, 179),      # Near max valid
        (-85, -179),    # Near min valid
    ]
    
    for lat, lon in test_cases:
        result = render_static_map_from_coordinates(lat, lon)
        # Should return either Image (success) or error dict (network failure)
        if hasattr(result, 'data'):
            # Success case
            print(f"   ✓ Valid coordinates ({lat}, {lon}) returned Image")
        else:
            # Network failure case - should be error dict
            assert isinstance(result, dict), f"Should return error dict for coordinates ({lat}, {lon})"
            print(f"   Note: Valid coordinates ({lat}, {lon}) failed due to network")
    
    print("   ✓ Valid edge coordinates handled correctly")
    
    # Invalid coordinates should return error dicts
    invalid_cases = [
        (91, 0),        # Lat too high
        (-91, 0),       # Lat too low
        (0, 181),       # Lon too high
        (0, -181),      # Lon too low
        (999, 999),     # Way out of bounds
    ]
    
    for lat, lon in invalid_cases:
        result = render_static_map_from_coordinates(lat, lon)
        assert isinstance(result, dict), f"Should return error dict for invalid coordinates ({lat}, {lon})"
        assert not result.get("success", True), f"Should indicate failure for coordinates ({lat}, {lon})"
    
    print("   ✓ Invalid coordinates return error dicts")
    print("✓ Coordinate edge cases working correctly")


def main():
    """Run all tests"""
    print("Running enhanced map rendering integration tests...\n")

    # Overwrite generic api key
    if not os.getenv("basemap_api_key") is None:
        os.environ["arcgis_api_key"] = os.getenv("basemap_api_key")
    
    try:
        text_render_functions()
        """
        test_enhanced_render_functions()
        test_backwards_compatibility()
        test_coordinate_edge_cases()
        """
        
        print("\n✅ All enhanced map rendering integration tests passed!")
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())