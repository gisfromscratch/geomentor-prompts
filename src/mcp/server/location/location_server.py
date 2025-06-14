from mcp.server.fastmcp import FastMCP
import requests
from typing import Dict, Optional
from location_config import ArcGISApiKeyManager

# Create an MCP server
mcp = FastMCP(name="Location MCP Demo", 
              description="A MCP demo server for location-based services",
              version="1.0.0",
              port=8000)


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
    
    # Add API key to parameters if provided
    ArcGISApiKeyManager.add_key_to_params(params, api_key)
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("candidates") and len(data["candidates"]) > 0:
            candidate = data["candidates"][0]
            
            return {
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

def reverse_geocode_coordinates(latitude: float, longitude: float, api_key: Optional[str] = None) -> Dict:
    """
    Reverse geocode coordinates using ArcGIS Location Platform Reverse Geocoding Services
    
    Args:
        latitude: The latitude coordinate
        longitude: The longitude coordinate
        api_key: Optional API key for ArcGIS services (uses free service if not provided)
    
    Returns:
        Dictionary containing reverse geocoded result with address and metadata
    """
    # ArcGIS World Geocoding Service reverse geocoding endpoint
    base_url = "https://geocode-api.arcgis.com/arcgis/rest/services/World/GeocodeServer/reverseGeocode"
    
    params = {
        "location": f"{longitude},{latitude}",  # ArcGIS expects x,y (lon,lat) format
        "f": "json",
        "outSR": "4326",  # WGS84 spatial reference
        "returnIntersection": "false"
    }
    
    # Add API key to parameters if provided
    ArcGISApiKeyManager.add_key_to_params(params, api_key)
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("address"):
            address_info = data["address"]
            
            return {
                "success": True,
                "coordinates": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "formatted_address": address_info.get("Match_addr", ""),
                "address_components": {
                    "street": address_info.get("Address", ""),
                    "city": address_info.get("City", ""),
                    "state": address_info.get("Region", ""),
                    "postal_code": address_info.get("Postal", ""),
                    "country": address_info.get("CountryCode", "")
                },
                "location_type": data.get("location", {}).get("spatialReference", {}).get("wkid", ""),
                "raw_response": data
            }
        else:
            return {
                "success": False,
                "coordinates": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "error": "No reverse geocoding results found",
                "formatted_address": None
            }
            
    except requests.RequestException as e:
        return {
            "success": False,
            "coordinates": {
                "latitude": latitude,
                "longitude": longitude
            },
            "error": f"Reverse geocoding request failed: {str(e)}",
            "formatted_address": None
        }
    except Exception as e:
        return {
            "success": False,
            "coordinates": {
                "latitude": latitude,
                "longitude": longitude
            },
            "error": f"Reverse geocoding error: {str(e)}",
            "formatted_address": None
        }

def get_elevation(latitude: float, longitude: float, api_key: Optional[str] = None) -> Dict:
    """
    Get elevation data for coordinates using ArcGIS Location Platform Elevation Services
    
    Args:
        latitude: The latitude coordinate
        longitude: The longitude coordinate
        api_key: Optional API key for ArcGIS services (uses free service if not provided)
    
    Returns:
        Dictionary containing elevation result with metadata
    """
    # ArcGIS Location Platform Elevation Service endpoint
    base_url = "https://elevation-api.arcgis.com/arcgis/rest/services/WorldElevation/Terrain/ImageServer/identify"
    
    params = {
        "f": "json",
        "geometry": f"{longitude},{latitude}",
        "geometryType": "esriGeometryPoint",
        "returnGeometry": "false",
        "returnCatalogItems": "false"
    }
    
    # Add API key to parameters if provided
    ArcGISApiKeyManager.add_key_to_params(params, api_key)
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("value") is not None:
            # Extract elevation data from response
            elevation_m = data["value"]
            
            if elevation_m is not None:
                # Convert to feet as well for convenience
                elevation_ft = elevation_m * 3.28084
                
                return {
                    "success": True,
                    "coordinates": {
                        "latitude": latitude,
                        "longitude": longitude
                    },
                    "elevation": {
                        "meters": round(elevation_m, 2),
                        "feet": round(elevation_ft, 2)
                    },
                    "data_source": "ArcGIS Location Platform Elevation Service",
                    "raw_response": data
                }
            
            return {
                "success": False,
                "coordinates": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "error": "No elevation value in response",
                "elevation": None
            }
        else:
            return {
                "success": False,
                "coordinates": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "error": "No elevation data found in response",
                "elevation": None
            }
            
    except requests.RequestException as e:
        return {
            "success": False,
            "coordinates": {
                "latitude": latitude,
                "longitude": longitude
            },
            "error": f"Elevation request failed: {str(e)}",
            "elevation": None
        }
    except Exception as e:
        return {
            "success": False,
            "coordinates": {
                "latitude": latitude,
                "longitude": longitude
            },
            "error": f"Elevation error: {str(e)}",
            "elevation": None
        }

@mcp.tool()
def get_elevation_for_coordinates(latitude: float, longitude: float) -> Dict:
    """
    Get elevation data for coordinates
    
    Args:
        latitude: The latitude coordinate (e.g., 37.4419)
        longitude: The longitude coordinate (e.g., -122.1430)
        
    Returns:
        Elevation data with coordinates and metadata
    """
    return get_elevation(latitude, longitude)

@mcp.tool()
def get_elevation_for_address(address: str) -> Dict:
    """
    Get elevation data for an address by first geocoding it
    
    Args:
        address: The address string to get elevation for
        
    Returns:
        Elevation data with coordinates and metadata
    """
    # First geocode the address
    geocode_result = geocode_address(address)
    if not geocode_result["success"]:
        return {
            "success": False,
            "address": address,
            "error": f"Failed to geocode address: {geocode_result['error']}",
            "elevation": None
        }
    
    # Get elevation for the geocoded coordinates
    coords = geocode_result["coordinates"]
    elevation_result = get_elevation(coords["latitude"], coords["longitude"])
    
    # Combine the results
    if elevation_result["success"]:
        return {
            "success": True,
            "address": address,
            "formatted_address": geocode_result["formatted_address"],
            "coordinates": coords,
            "elevation": elevation_result["elevation"],
            "data_source": elevation_result["data_source"],
            "geocoding_score": geocode_result["score"]
        }
    else:
        return {
            "success": False,
            "address": address,
            "formatted_address": geocode_result["formatted_address"],
            "coordinates": coords,
            "error": elevation_result["error"],
            "elevation": None
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
def reverse_geocode(latitude: float, longitude: float) -> Dict:
    """
    Reverse geocode coordinates to get address and location information
    
    Args:
        latitude: The latitude coordinate (e.g., 37.4419)
        longitude: The longitude coordinate (e.g., -122.1430)
        
    Returns:
        Reverse geocoded result with address and metadata
    """
    return reverse_geocode_coordinates(latitude, longitude)

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
    geocode_result = geocode_address(address)
    if not geocode_result["success"]:
        return {"error": f"Geocoding failed for {address}: {geocode_result['error']}"}
    
    coords = geocode_result["coordinates"]
    lat, lon = coords["latitude"], coords["longitude"]
    
    # Generate URLs for different map services
    map_urls = {
        "google_maps": f"https://www.google.com/maps?q={lat},{lon}&z={zoom_level}",
        "openstreetmap": f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom={zoom_level}",
        "arcgis": f"https://www.arcgis.com/home/webmap/viewer.html?center={lon},{lat}&level={zoom_level}",
        "coordinates": f"{lat},{lon}",
        "formatted_address": geocode_result["formatted_address"]
    }
    
    return {
        "success": True,
        "address": address,
        "map_urls": map_urls,
        "embed_html": generate_map_embed_html(lat, lon, geocode_result["formatted_address"], zoom_level)
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
    geocode_result = geocode_address(address)
    if not geocode_result["success"]:
        return {
            "success": False,
            "error": f"Failed to geocode address: {geocode_result['error']}"
        }
    
    map_data = generate_map_url(address, zoom_level)
    if "error" in map_data:
        return {"success": False, "error": map_data["error"]}
    
    coords = geocode_result["coordinates"]
    
    display_package = {
        "success": True,
        "address": address,
        "formatted_address": geocode_result["formatted_address"],
        "coordinates": coords,
        "map_urls": map_data["map_urls"],
        "geocoding_score": geocode_result["score"]
    }
    
    if include_html:
        display_package["embed_html"] = map_data["embed_html"]
        display_package["markdown_map"] = f"📍 **{geocode_result['formatted_address']}**\n\n🗺️ [View on Google Maps]({map_data['map_urls']['google_maps']})\n📐 Coordinates: `{coords['latitude']:.4f}, {coords['longitude']:.4f}`\n🎯 Accuracy Score: {geocode_result['score']}/100"
    
    return display_package

@mcp.tool()
def display_location_with_elevation(address: str, include_html: bool = True, zoom_level: int = 15) -> Dict:
    """
    Complete tool for displaying a geocoded location with elevation data in the chat UI
    
    Args:
        address: The address to display on map with elevation
        include_html: Whether to include HTML embed code (default: True)
        zoom_level: Map zoom level (default: 15)
        
    Returns:
        Complete display package including coordinates, elevation, URLs and embed code
    """
    # Get geocoding and elevation data
    elevation_result = get_elevation_for_address(address)
    if not elevation_result["success"]:
        return {
            "success": False,
            "error": f"Failed to get elevation for address: {elevation_result['error']}"
        }
    
    # Get map data
    map_data = generate_map_url(address, zoom_level)
    if "error" in map_data:
        return {"success": False, "error": map_data["error"]}
    
    coords = elevation_result["coordinates"]
    elevation = elevation_result["elevation"]
    
    display_package = {
        "success": True,
        "address": address,
        "formatted_address": elevation_result["formatted_address"],
        "coordinates": coords,
        "elevation": elevation,
        "map_urls": map_data["map_urls"],
        "geocoding_score": elevation_result.get("geocoding_score", 0)
    }
    
    if include_html:
        display_package["embed_html"] = map_data["embed_html"]
        display_package["markdown_map"] = f"📍 **{elevation_result['formatted_address']}**\n\n🗺️ [View on Google Maps]({map_data['map_urls']['google_maps']})\n📐 Coordinates: `{coords['latitude']:.4f}, {coords['longitude']:.4f}`\n⛰️ Elevation: `{elevation['meters']} m ({elevation['feet']} ft)`\n🎯 Accuracy Score: {elevation_result.get('geocoding_score', 0)}/100"
    
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
    geocode_result = geocode_address(address)
    if geocode_result["success"]:
        coords = geocode_result["coordinates"]
        return f"Location: {geocode_result['formatted_address']}\nCoordinates: {coords['latitude']}, {coords['longitude']}\nScore: {geocode_result['score']}"
    else:
        return f"Geocoding failed for {address}: {geocode_result['error']}"

# Add a reverse geocoding resource for displaying address data from coordinates
@mcp.resource("reverse_geocode://{latitude},{longitude}")
def get_reverse_geocode_info(latitude: str, longitude: str) -> str:
    """Get address information for coordinates"""
    try:
        lat = float(latitude)
        lon = float(longitude)
        reverse_result = reverse_geocode_coordinates(lat, lon)
        if reverse_result["success"]:
            address_components = reverse_result["address_components"]
            return f"Address: {reverse_result['formatted_address']}\nCoordinates: {lat}, {lon}\nStreet: {address_components['street']}\nCity: {address_components['city']}\nState: {address_components['state']}\nCountry: {address_components['country']}"
        else:
            return f"Reverse geocoding failed for {lat}, {lon}: {reverse_result['error']}"
    except ValueError:
        return f"Invalid coordinates: {latitude}, {longitude}"
    
# Add an elevation resource for displaying elevation data from coordinates
@mcp.resource("elevation://{latitude},{longitude}")
def get_elevation_info(latitude: str, longitude: str) -> str:
    """Get elevation information for coordinates"""
    try:
        lat = float(latitude)
        lon = float(longitude)
        elevation_result = get_elevation(lat, lon)
        if elevation_result["success"]:
            elevation = elevation_result["elevation"]
            return f"Elevation at {lat}, {lon}:\n{elevation['meters']} meters ({elevation['feet']} feet)\nData source: {elevation_result['data_source']}"
        else:
            return f"Elevation lookup failed for {lat}, {lon}: {elevation_result['error']}"
    except ValueError:
        return f"Invalid coordinates: {latitude}, {longitude}"

# Add an elevation resource for addresses
@mcp.resource("elevation_address://{address}")
def get_elevation_address_info(address: str) -> str:
    """Get elevation information for an address"""
    elevation_result = get_elevation_for_address(address)
    if elevation_result["success"]:
        coords = elevation_result["coordinates"]
        elevation = elevation_result["elevation"]
        return f"Elevation for {elevation_result['formatted_address']}:\nCoordinates: {coords['latitude']}, {coords['longitude']}\nElevation: {elevation['meters']} meters ({elevation['feet']} feet)\nGeocoding Score: {elevation_result.get('geocoding_score', 0)}/100"
    else:
        return f"Elevation lookup failed for {address}: {elevation_result['error']}"


if __name__ == "__main__":
    # Start the server locally
    mcp.run(transport="sse")