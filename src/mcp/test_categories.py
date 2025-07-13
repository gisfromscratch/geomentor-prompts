#!/usr/bin/env python3
"""
Test script for categories functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'server', 'location'))

from location_server import fetch_place_categories, get_cached_categories, list_categories

def test_fetch_categories_structure():
    """Test that fetch_place_categories function has correct structure"""
    print("Testing fetch_place_categories structure...")
    
    # Test that function exists and is callable
    assert callable(fetch_place_categories), "fetch_place_categories should be callable"
    
    result = fetch_place_categories()
    assert "success" in result, "Result should have success field"
    
    # Either success with categories or failure with error
    if result["success"]:
        assert "categories" in result, "Should have categories when successful"
        assert "total_count" in result, "Should have total_count when successful"
        assert isinstance(result["categories"], list), "Categories should be a list"
        assert result["total_count"] >= 0, "Total count should be non-negative"
        
        # If categories found, check structure of first category
        if result["categories"]:
            category = result["categories"][0]
            assert "categoryId" in category or "categoryId" in str(category), "Category should have categoryId"
            assert "label" in category or "label" in str(category), "Category should have label"
    else:
        assert "error" in result, "Should have error message when unsuccessful"
    
    print("✓ fetch_place_categories structure working correctly")

def test_cached_categories():
    """Test category caching functionality"""
    print("Testing category caching...")
    
    # Test that function exists and is callable
    assert callable(get_cached_categories), "get_cached_categories should be callable"
    
    # First call should populate cache
    result1 = get_cached_categories()
    assert "success" in result1, "Result should have success field"
    
    # Second call should use cache (should be same result)
    result2 = get_cached_categories()
    assert "success" in result2, "Result should have success field"
    
    # Results should be identical (same object from cache)
    assert result1 == result2, "Cached results should be identical"
    
    print("✓ Category caching working correctly")

def test_list_categories_tool():
    """Test list_categories tool functionality"""
    print("Testing list_categories tool...")
    
    # Test that function exists and is callable
    assert callable(list_categories), "list_categories should be callable"
    
    # Test basic call without filters
    result = list_categories()
    assert "success" in result, "Result should have success field"
    assert "categories" in result, "Should have categories field"
    assert "total_count" in result, "Should have total_count field"
    assert "filters_applied" in result, "Should have filters_applied field"
    assert "usage_info" in result, "Should have usage_info field"
    
    # Test with level filter
    result_level = list_categories(level=1)
    assert "success" in result_level, "Result should have success field"
    assert result_level["filters_applied"]["level"] == 1, "Level filter should be preserved"
    
    # Test with parent category filter
    result_parent = list_categories(parent_category_id="test")
    assert "success" in result_parent, "Result should have success field"
    assert result_parent["filters_applied"]["parent_category_id"] == "test", "Parent filter should be preserved"
    
    print("✓ list_categories tool working correctly")

def test_parameter_validation():
    """Test parameter validation in list_categories"""
    print("Testing list_categories parameter validation...")
    
    # Test with valid parameters
    result = list_categories(level=1, parent_category_id=None)
    assert "success" in result, "Result should have success field"
    
    # Test that it handles None values gracefully
    result_none = list_categories(level=None, parent_category_id=None)
    assert "success" in result_none, "Result should handle None values"
    
    print("✓ Parameter validation working correctly")

def test_usage_info():
    """Test that usage information is provided"""
    print("Testing usage information...")
    
    result = list_categories()
    if result["success"]:
        assert "usage_info" in result, "Should provide usage information"
        usage_info = result["usage_info"]
        assert "description" in usage_info, "Should have description"
        assert "example" in usage_info, "Should have example"
        
        # Check that usage info mentions the relevant tools
        description = usage_info["description"].lower()
        assert "find_places" in description, "Should mention find_places tool"
        assert "categoryid" in description, "Should mention categoryId parameter"
    
    print("✓ Usage information working correctly")

def main():
    """Run all categories tests"""
    print("Running categories functionality tests...\n")
    
    try:
        test_fetch_categories_structure()
        test_cached_categories()
        test_list_categories_tool()
        test_parameter_validation()
        test_usage_info()
        
        print("\n✅ All categories tests passed! Categories functionality is working correctly.")
        return 0
        
    except Exception as e:
        print(f"\n❌ Categories test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())