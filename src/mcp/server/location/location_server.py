from mcp.server.fastmcp import FastMCP
import requests
import json
from typing import Dict, Optional

# Create an MCP server
mcp = FastMCP(name="Location MCP Demo", 
              description="A MCP demo server for location-based services",
              version="1.0.0",
              port=8000)

# Global storage for geocoded results (in a real implementation, this would be a database)
geocoded_metadata = {}

def geocode_address(address: str, api_key: Optional[str] = None) -> Dict:
    """
    Geocode an address using ArcGIS Location Platform Geocoding Services
    
    Args:
        address: The address string to geocode
        api_key: Optional API key for ArcGIS services (uses free service if not provided)
    
    Returns:
        Dictionary containing geocoded result with coordinates and metadata
    """
    # ArcGIS World Geocoding Service endpoint
    base_url = "https://geocode-api.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates"
    
    params = {
        "singleLine": address,
        "f": "json",
        "outFields": "Addr_type,Type,PlaceName,Place_addr,Phone,URL,Rank",
        "maxLocations": 1
    }
    
    # Add API key if provided
    if api_key:
        params["token"] = api_key
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("candidates") and len(data["candidates"]) > 0:
            candidate = data["candidates"][0]
            
            result = {
                "success": True,
                "address": address,
                "formatted_address": candidate.get("address", ""),
                "coordinates": {
                    "latitude": candidate["location"]["y"],
                    "longitude": candidate["location"]["x"]
                },
                "score": candidate.get("score", 0),
                "attributes": candidate.get("attributes", {}),
                "raw_response": candidate
            }
            
            # Store in metadata
            geocoded_metadata[address] = result
            
            return result
        else:
            return {
                "success": False,
                "address": address,
                "error": "No geocoding results found",
                "coordinates": None
            }
            
    except requests.RequestException as e:
        return {
            "success": False,
            "address": address,
            "error": f"Geocoding request failed: {str(e)}",
            "coordinates": None
        }
    except Exception as e:
        return {
            "success": False,
            "address": address,
            "error": f"Geocoding error: {str(e)}",
            "coordinates": None
        }

@mcp.tool()
def geocode(address: str) -> Dict:
    """
    Geocode an address and return coordinates with metadata
    
    Args:
        address: The address string to geocode
        
    Returns:
        Geocoded result with coordinates and metadata
    """
    return geocode_address(address)

@mcp.tool()
def get_geocoded_metadata(address: Optional[str] = None) -> Dict:
    """
    Retrieve stored geocoded metadata
    
    Args:
        address: Optional specific address to retrieve. If None, returns all stored data
        
    Returns:
        Geocoded metadata for the address or all stored metadata
    """
    if address:
        return geocoded_metadata.get(address, {"error": "Address not found in metadata"})
    else:
        return {
            "total_geocoded": len(geocoded_metadata),
            "addresses": list(geocoded_metadata.keys()),
            "metadata": geocoded_metadata
        }

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

# Add a geocoding resource for displaying location data
@mcp.resource("location://{address}")
def get_location_info(address: str) -> str:
    """Get location information for an address"""
    if address in geocoded_metadata:
        result = geocoded_metadata[address]
        if result["success"]:
            coords = result["coordinates"]
            return f"Location: {result['formatted_address']}\nCoordinates: {coords['latitude']}, {coords['longitude']}\nScore: {result['score']}"
        else:
            return f"Geocoding failed for {address}: {result['error']}"
    else:
        return f"No geocoding data available for {address}. Use the geocode tool first."
    

if __name__ == "__main__":
    # Start the server locally
    mcp.run(transport="sse")