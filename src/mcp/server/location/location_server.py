from mcp.server.fastmcp import FastMCP
import os
import requests
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
    elif any(env_key.lower() == "arcgis_api_key" for env_key in os.environ):
        # Use API key from environment variable if available (case-insensitive)
        for key, value in os.environ.items():
            if key.lower() == "arcgis_api_key":
                params["token"] = value
                break
    
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

@mcp.tool()
def generate_map_url(address: str, zoom_level: int = 15) -> Dict:
    """
    Generate map URLs for displaying geocoded locations in chat UI
    
    Args:
        address: The geocoded address to generate map for
        zoom_level: Map zoom level (default: 15)
        
    Returns:
        Dictionary containing various map service URLs
    """
    if address not in geocoded_metadata:
        return {"error": "Address not found in geocoded metadata. Geocode it first."}
    
    result = geocoded_metadata[address]
    if not result["success"]:
        return {"error": f"Geocoding failed for {address}: {result['error']}"}
    
    coords = result["coordinates"]
    lat, lon = coords["latitude"], coords["longitude"]
    
    # Generate URLs for different map services
    map_urls = {
        "google_maps": f"https://www.google.com/maps?q={lat},{lon}&z={zoom_level}",
        "openstreetmap": f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom={zoom_level}",
        "arcgis": f"https://www.arcgis.com/home/webmap/viewer.html?center={lon},{lat}&level={zoom_level}",
        "leaflet_embed": f"https://maps.wikimedia.org/en/coord/{lat},{lon},{zoom_level}",
        "coordinates": f"{lat},{lon}",
        "formatted_address": result["formatted_address"]
    }
    
    return {
        "success": True,
        "address": address,
        "map_urls": map_urls,
        "embed_html": generate_map_embed_html(lat, lon, result["formatted_address"], zoom_level)
    }

def generate_map_embed_html(lat: float, lon: float, address: str, zoom: int = 15) -> str:
    """Generate HTML for embedding a map in chat UI"""
    return f"""
    <div style="width: 100%; height: 300px; border: 1px solid #ccc; border-radius: 5px; overflow: hidden;">
        <iframe 
            width="100%" 
            height="100%" 
            frameborder="0" 
            scrolling="no" 
            marginheight="0" 
            marginwidth="0" 
            src="https://www.openstreetmap.org/export/embed.html?bbox={lon-0.01},{lat-0.01},{lon+0.01},{lat+0.01}&amp;layer=mapnik&amp;marker={lat},{lon}"
            title="Map showing {address}">
        </iframe>
        <div style="padding: 8px; background: #f5f5f5; font-size: 12px; text-align: center;">
            📍 {address} ({lat:.4f}, {lon:.4f})
            <br>
            <a href="https://www.google.com/maps?q={lat},{lon}" target="_blank" style="color: #1976d2;">View in Google Maps</a>
        </div>
    </div>
    """

@mcp.tool()
def display_location_on_map(address: str, include_html: bool = True, zoom_level: int = 15) -> Dict:
    """
    Complete tool for displaying a geocoded location on a map in the chat UI
    
    Args:
        address: The address to display on map
        include_html: Whether to include HTML embed code (default: True)
        zoom_level: Map zoom level (default: 15)
        
    Returns:
        Complete map display package including URLs and embed code
    """
    # First geocode if not already done
    if address not in geocoded_metadata:
        geocode_result = geocode_address(address)
        if not geocode_result["success"]:
            return {
                "success": False,
                "error": f"Failed to geocode address: {geocode_result['error']}"
            }
    
    # Generate map URLs and embed code
    map_data = generate_map_url(address, zoom_level)
    if "error" in map_data:
        return {"success": False, "error": map_data["error"]}
    
    result = geocoded_metadata[address]
    coords = result["coordinates"]
    
    display_package = {
        "success": True,
        "address": address,
        "formatted_address": result["formatted_address"],
        "coordinates": coords,
        "map_urls": map_data["map_urls"],
        "geocoding_score": result["score"]
    }
    
    if include_html:
        display_package["embed_html"] = map_data["embed_html"]
        display_package["markdown_map"] = f"📍 **{result['formatted_address']}**\n\n🗺️ [View on Google Maps]({map_data['map_urls']['google_maps']})\n📐 Coordinates: `{coords['latitude']:.4f}, {coords['longitude']:.4f}`\n🎯 Accuracy Score: {result['score']}/100"
    
    return display_package

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