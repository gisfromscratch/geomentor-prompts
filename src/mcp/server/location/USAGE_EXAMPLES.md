#!/usr/bin/env python3
"""
Example usage of the ArcGIS Online search functionality
This demonstrates how to use the new search_webmaps_and_layers tool
"""

# Example 1: Search for forest-related web maps
example_1 = {
    "query": "forest conservation",
    "item_types": ["Web Map"],
    "num": 10,
    "sort_field": "avgRating",
    "sort_order": "desc"
}

print("Example 1: Search for forest conservation web maps")
print("Tool call: search_webmaps_and_layers(")
for key, value in example_1.items():
    print(f"    {key}={repr(value)},")
print(")")
print()

# Example 2: Search for feature layers about population in a specific area
example_2 = {
    "query": "population demographics",
    "item_types": ["Feature Layer", "Feature Service"],
    "bbox": "-125,25,-66,50",  # Continental US bounds
    "num": 25,
    "sort_field": "numViews"
}

print("Example 2: Search for population feature layers in Continental US")
print("Tool call: search_webmaps_and_layers(")
for key, value in example_2.items():
    print(f"    {key}={repr(value)},")
print(")")
print()

# Example 3: General search with pagination
example_3 = {
    "query": "climate change",
    "start": 1,
    "num": 50
}

print("Example 3: General climate change search with pagination")
print("Tool call: search_webmaps_and_layers(")
for key, value in example_3.items():
    print(f"    {key}={repr(value)},")
print(")")
print()

# Example 4: Search all types sorted by views
example_4 = {
    "query": "transportation",
    "sort_field": "numViews",
    "sort_order": "desc",
    "num": 20
}

print("Example 4: Transportation content sorted by popularity")
print("Tool call: search_webmaps_and_layers(")
for key, value in example_4.items():
    print(f"    {key}={repr(value)},")
print(")")
print()

print("Expected Response Structure:")
print("""
{
    "success": true,
    "search_query": { ... },
    "results": {
        "total_results": 150,
        "returned_results": 20,
        "items": [
            {
                "id": "abc123",
                "title": "Global Transportation Networks",
                "owner": "transport_dept", 
                "type": "Web Map",
                "description": "Comprehensive transportation infrastructure data",
                "num_views": 45678,
                "avg_rating": 4.8,
                "portal_item_url": "https://www.arcgis.com/home/item.html?id=abc123",
                "service_url": "https://services.arcgis.com/.../FeatureServer",
                "feature_server_url": "https://services.arcgis.com/.../FeatureServer"
            }
            // ... more items
        ]
    },
    "type_breakdown": {
        "Web Map": 12,
        "Feature Service": 8  
    },
    "chat_summary": "Found 150 items matching 'transportation'. Top results: Global Transportation Networks (Web Map), Transit Routes (Feature Service), ..."
}
""")

print("\nKey Benefits:")
print("✅ Direct portal item links for easy access")  
print("✅ FeatureServer URLs for programmatic access to data")
print("✅ Rich metadata for informed decision making")
print("✅ Flexible filtering and sorting options")
print("✅ Spatial filtering with bounding box support")
print("✅ Chat-friendly summaries for conversational interfaces")
print("✅ Comprehensive error handling")
print("✅ Pagination support for large result sets")