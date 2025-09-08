from datetime import datetime, UTC
from location_config import ArcGISApiKeyManager
from location_server_class import LocationServer
from mcp.server.fastmcp import FastMCP
import requests
from typing import Dict, List, Optional


# Create a simple MCP server instance for tool registration
mcp = FastMCP("Location Search Server")


def search_arcgis_online(
    query: str = "",
    item_types: Optional[List[str]] = None,
    bbox: Optional[str] = None,
    start: int = 1,
    num: int = 50,
    sort_field: Optional[str] = None,
    sort_order: str = "desc",
    count_fields: Optional[str] = None,
    count_size: Optional[int] = None
) -> Dict:
    """
    Search ArcGIS Online for webmaps and layers using the ArcGIS REST API search endpoint.
    
    Args:
        query: Search string (default: empty for all items)
        item_types: List of item types to search for (e.g., ["Web Map", "Feature Layer"])
        bbox: Bounding box to filter results spatially (format: "xmin,ymin,xmax,ymax")
        start: Starting position for pagination (default: 1)
        num: Number of results to return per page (1-100, default: 50)
        sort_field: Field to sort by (e.g., "avgRating", "numViews", "title", "created", "modified")
        sort_order: Sort order "asc" or "desc" (default: "desc")
        count_fields: Fields to count/aggregate (optional)
        count_size: Maximum count size for aggregations (optional)
        
    Returns:
        Dictionary containing search results with metadata, portal links, and service URLs
    """
    # ArcGIS Online search endpoint
    base_url = "https://www.arcgis.com/sharing/rest/search"
    
    # Build query string
    query_parts = []
    if query.strip():
        query_parts.append(query.strip())
    
    # Combine query parts
    search_query = " AND ".join(query_parts) if query_parts else "*"

    # Add item type filters
    item_type_query_parts = []
    if item_types:
        for item_type in item_types:
            item_type_query_parts.append(f'type:"{item_type}"')
    
    item_type_query = " OR ".join(item_type_query_parts) if item_type_query_parts else None
    if item_type_query:
        search_query = f"({search_query}) AND ({item_type_query})"
    
    # Build parameters
    params = {
        "q": search_query,
        "f": "json",
        "start": max(1, start),
        "num": min(max(1, num), 100),  # Clamp between 1 and 100
        "sortOrder": sort_order if sort_order in ["asc", "desc"] else "desc"
    }
    
    # Add optional parameters
    if bbox:
        params["bbox"] = bbox
    if sort_field:
        params["sortField"] = sort_field
    if count_fields:
        params["countFields"] = count_fields
    if count_size:
        params["countSize"] = count_size
    
    # Note: ArcGIS Online search does not require authentication for public content
    # API key is only needed for private content or higher rate limits
    api_key = ArcGISApiKeyManager.get_api_key()
    if api_key:
        params["token"] = api_key
    
    try:
        response = requests.get(base_url, params=params, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        
        if "results" in data:
            items = []
            for result in data["results"]:
                # Extract metadata
                item_info = {
                    "id": result.get("id", ""),
                    "title": result.get("title", "Unknown Title"),
                    "owner": result.get("owner", "Unknown Owner"),
                    "type": result.get("type", "Unknown Type"),
                    "description": result.get("description", ""),
                    "snippet": result.get("snippet", ""),
                    "tags": result.get("tags", []),
                    "thumbnail": result.get("thumbnail", ""),
                    "access": result.get("access", ""),
                    "num_views": result.get("numViews", 0),
                    "avg_rating": result.get("avgRating", 0),
                    "num_ratings": result.get("numRatings", 0),
                    "created": result.get("created", 0),
                    "modified": result.get("modified", 0),
                    "lastViewed": result.get("lastViewed", 0),
                    "size": result.get("size", 0)
                }

                # Convert Esri unix timestamps to ISO format
                for time_field in ["created", "modified", "lastViewed"]:
                    if item_info[time_field]:
                        item_info[time_field] = datetime.fromtimestamp(item_info[time_field] * 1e-3, UTC).isoformat()

                # Add portal item link
                if result.get("id"):
                    # Default to ArcGIS Online, but could be customized for Enterprise
                    portal_base = "https://www.arcgis.com"
                    item_info["portal_item_url"] = f"{portal_base}/home/item.html?id={result['id']}"
                
                # Add service URL for feature layers and other service types
                service_types = ["Feature Service", "Map Service", "Image Service", 
                               "Feature Layer", "Scene Service", "Vector Tile Service"]
                if result.get("type") in service_types and result.get("url"):
                    item_info["service_url"] = result["url"]
                    # For Feature Services, ensure the URL points to FeatureServer
                    if result.get("type") in ["Feature Service", "Feature Layer"]:
                        service_url = result["url"]
                        if "/FeatureServer" not in service_url:
                            if "/MapServer" in service_url:
                                # Handle both /MapServer and /MapServer/0 patterns
                                service_url = service_url.split("/MapServer")[0] + "/FeatureServer"
                            else:
                                service_url = service_url.rstrip("/") + "/FeatureServer"
                        elif "/FeatureServer/" in service_url:
                            # URL already points to a specific layer, keep the FeatureServer base
                            service_url = service_url.split("/FeatureServer/")[0] + "/FeatureServer"
                        item_info["feature_server_url"] = service_url
                
                # Add raw data for advanced users
                item_info["raw_data"] = result
                
                items.append(item_info)
            
            # Check if we actually have results  
            response_data = {
                "success": True,
                "search_query": {
                    "query": search_query,
                    "original_query": query,
                    "item_types": item_types,
                    "bbox": bbox,
                    "start": start,
                    "num": num,
                    "sort_field": sort_field,
                    "sort_order": sort_order
                },
                "results": {
                    "total_results": data.get("total", 0),
                    "returned_results": len(items),
                    "start": data.get("start", start),
                    "num": data.get("num", num),
                    "items": items
                },
                "query_info": data.get("queryInfo", {}),
                "aggregations": data.get("aggregations", {}),
                "raw_response": data
            }
            
            # Add message if no results found
            if data.get("total", 0) == 0:
                response_data["message"] = "No results found for the specified criteria"
                
            return response_data
        else:
            return {
                "success": True,
                "search_query": {
                    "query": search_query,
                    "original_query": query,
                    "item_types": item_types,
                    "bbox": bbox,
                    "start": start,
                    "num": num,
                    "sort_field": sort_field,
                    "sort_order": sort_order
                },
                "results": {
                    "total_results": 0,
                    "returned_results": 0,
                    "start": start,
                    "num": num,
                    "items": []
                },
                "message": "No results found for the specified criteria"
            }
            
    except requests.RequestException as e:
        return {
            "success": False,
            "search_query": {
                "query": search_query,
                "original_query": query,
                "item_types": item_types
            },
            "error": f"ArcGIS Online search request failed: {str(e)}",
            "results": {
                "total_results": 0,
                "returned_results": 0,
                "items": []
            }
        }
    except Exception as e:
        return {
            "success": False,
            "search_query": {
                "query": search_query,
                "original_query": query,
                "item_types": item_types
            },
            "error": f"ArcGIS Online search error: {str(e)}",
            "results": {
                "total_results": 0,
                "returned_results": 0,
                "items": []
            }
        }


@mcp.tool()
def search_webmaps_and_layers(
    query: str = "", 
    item_types: Optional[List[str]] = None,
    bbox: Optional[str] = None, 
    start: int = 1, 
    num: int = 50,
    sort_field: Optional[str] = None,
    sort_order: str = "desc"
) -> Dict:
    """
    Search ArcGIS Online for webmaps and layers. Returns items with portal links and service URLs.
    
    Args:
        query: Search keywords (e.g., "forest", "population", "traffic")
        item_types: List of item types to search for. Common types:
                   - ["Web Map"] for webmaps only
                   - ["Feature Collection", "Feature Service"] for feature layers
                   - ["Map Service", "Image Service"] for other services
                   If not specified, searches all types
        bbox: Bounding box to filter results spatially (format: "xmin,ymin,xmax,ymax" in WGS84)
        start: Starting position for pagination (default: 1)
        num: Number of results per page (1-100, default: 50)
        sort_field: Field to sort by ("avgRating", "numViews", "title", "created", "modified")
        sort_order: Sort order "asc" or "desc" (default: "desc")
        
    Returns:
        Dictionary containing search results with metadata, portal item links, and service URLs
    """
    
    # Set default item types if not specified
    if item_types is None:
        item_types = ["Web Map", "Feature Layer", "Feature Service", "Map Service"]
    
    # Call the core search function
    result = search_arcgis_online(
        query=query,
        item_types=item_types,
        bbox=bbox,
        start=start,
        num=num,
        sort_field=sort_field,
        sort_order=sort_order
    )
    
    if result["success"] and result["results"]["items"]:
        # Add chat-friendly summary
        items = result["results"]["items"]
        total_results = result["results"]["total_results"]
        
        summary_parts = []
        summary_parts.append(f"Found {total_results} items")
        
        if query.strip():
            summary_parts.append(f"matching '{query}'")
        
        if item_types and len(item_types) < 4:  # If not searching all default types
            type_str = "', '".join(item_types)
            summary_parts.append(f"of type '{type_str}'")
        
        if bbox:
            summary_parts.append("within specified geographic area")
            
        summary = " ".join(summary_parts) + "."
        
        # Add details about top results
        if len(items) >= 3:
            top_items = [f"{item['title']} ({item['type']})" for item in items[:3]]
            summary += f" Top results: {', '.join(top_items)}"
        elif len(items) > 0:
            top_items = [f"{item['title']} ({item['type']})" for item in items]
            summary += f" Results: {', '.join(top_items)}"
            
        result["chat_summary"] = summary
        
        # Count by type for additional insight
        type_counts = {}
        for item in items:
            item_type = item.get("type", "Unknown")
            type_counts[item_type] = type_counts.get(item_type, 0) + 1
        
        result["type_breakdown"] = type_counts
        
    else:
        # Handle no results case
        if result["success"]:
            summary_parts = ["No items found"]
            if query.strip():
                summary_parts.append(f"matching '{query}'")
            if item_types:
                type_str = "', '".join(item_types)
                summary_parts.append(f"of type '{type_str}'")
            if bbox:
                summary_parts.append("within specified geographic area")
                
            result["chat_summary"] = " ".join(summary_parts) + ". Try broader search terms or different item types."
        
    return result


if __name__ == "__main__":
    # Start the server using the stdio transport
    mcp.run(transport="stdio")