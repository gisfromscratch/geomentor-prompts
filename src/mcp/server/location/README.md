# Location Services Documentation

## Overview
The Location MCP Server includes geocoding, reverse geocoding, elevation data services, map display, routing functionality, nearby places search, and ArcGIS Online content search using ArcGIS Location Platform services to provide comprehensive location-based services including coordinate conversion, elevation information, point-of-interest discovery, and web map/layer search capabilities.

## Features
- **Address Geocoding**: Convert text addresses to latitude/longitude coordinates
- **Reverse Geocoding**: Convert latitude/longitude coordinates to readable addresses
- **Elevation Services**: Get elevation data for coordinates or addresses
- **Routing & Directions**: Get turn-by-turn directions between locations with travel time and distance
- **Map Display**: Generate map URLs and embed HTML for various mapping services
- **Interactive Maps**: Generate embeddable maps for chat UI display
- **Static Basemap Tiles**: Fetch static map tiles from ArcGIS Location Platform basemaps
- **Visual Map Representation**: Generate PNG tile images for locations and coordinates
- **🆕 Smart Map Rendering**: Automatic zoom level and style selection based on location type
- **🆕 Location String Support**: Render maps directly from address/place strings with auto-geocoding
- **Nearby Places Search**: Find places of interest around a location with category filtering
- **🆕 ArcGIS Online Content Search**: Search for webmaps, layers, and services on ArcGIS Online
- **Metadata Storage**: Store geocoded, elevation, and routing results for efficient retrieval
- **Error Handling**: Robust error handling for failed requests
- **Resource Endpoints**: Access location, elevation, and places data through MCP resources
- **Chat UI Integration**: Display maps, elevation data, and directions in chat interfaces

## Tools Available

### `find_places(location: str, category: Optional[str] = None, radius: int = 1000, max_results: int = 10)`
Find nearby places around a given location with optional category filtering.

**Parameters:**
- `location` (str): Address or location description to search around
- `category` (Optional[str]): Category filter (e.g., 'restaurant', 'gas_station', 'park', 'hotel', 'hospital')
- `radius` (int): Search radius in meters (default: 1000m, max: 50000m)
- `max_results` (int): Maximum number of results to return (default: 10, max: 50)

**Returns:**
```json
{
    "success": true,
    "search_query": {
        "location": "Original location input",
        "geocoded_address": "Standardized address",
        "coordinates": {"latitude": 37.4419, "longitude": -122.1430},
        "category_filter": "restaurant",
        "radius_meters": 1000,
        "max_results": 10
    },
    "results": {
        "total_found": 5,
        "places": [
            {
                "name": "Place Name",
                "place_id": "unique_id",
                "categories": ["restaurant", "food"],
                "address": "123 Main St, City, State",
                "coordinates": {"latitude": 37.4420, "longitude": -122.1431},
                "distance": 150,
                "phone": "+1-234-567-8900",
                "website": "https://example.com",
                "rating": 4.5,
                "price_level": "$$"
            }
        ]
    },
    "map_visualization": {
        "search_center_urls": {...},
        "search_area_html": "HTML for embedding map"
    },
    "chat_summary": "Found 5 places in category 'restaurant' within 1000m..."
}
```

### `find_places_by_coordinates(latitude: float, longitude: float, category: Optional[str] = None, radius: int = 1000, max_results: int = 10)`
Find nearby places around specific coordinates with optional category filtering.

**Parameters:**
- `latitude` (float): Latitude coordinate to search around
- `longitude` (float): Longitude coordinate to search around  
- `category` (Optional[str]): Category filter (e.g., 'restaurant', 'gas_station', 'park')
- `radius` (int): Search radius in meters (default: 1000m, max: 50000m)
- `max_results` (int): Maximum number of results to return (default: 10, max: 50)

**Returns:**
Similar structure to `find_places` but with coordinate-based search query information.

### `search_webmaps_and_layers(query: str = "", item_types: Optional[List[str]] = None, bbox: Optional[str] = None, start: int = 1, num: int = 50, sort_field: Optional[str] = None, sort_order: str = "desc")` 🆕
Search ArcGIS Online for webmaps and layers. Returns items with portal links and service URLs.

**Parameters:**
- `query` (str): Search keywords (e.g., "forest", "population", "traffic")
- `item_types` (Optional[List[str]]): List of item types to search for. Common types:
  - `["Web Map"]` for webmaps only
  - `["Feature Layer", "Feature Service"]` for feature layers
  - `["Map Service", "Image Service"]` for other services
  - If not specified, searches all types
- `bbox` (Optional[str]): Bounding box to filter results spatially (format: "xmin,ymin,xmax,ymax" in WGS84)
- `start` (int): Starting position for pagination (default: 1)
- `num` (int): Number of results per page (1-100, default: 50)
- `sort_field` (Optional[str]): Field to sort by ("avgRating", "numViews", "title", "created", "modified")
- `sort_order` (str): Sort order "asc" or "desc" (default: "desc")

**Returns:**
```json
{
    "success": true,
    "search_query": {
        "query": "forest AND type:\"Web Map\"",
        "original_query": "forest",
        "item_types": ["Web Map"],
        "bbox": null,
        "start": 1,
        "num": 50,
        "sort_field": "avgRating",
        "sort_order": "desc"
    },
    "results": {
        "total_results": 150,
        "returned_results": 50,
        "start": 1,
        "num": 50,
        "items": [
            {
                "id": "abc123def456",
                "title": "Global Forest Watch",
                "owner": "wri",
                "type": "Web Map",
                "description": "Real-time monitoring of global forest cover and loss",
                "snippet": "Interactive map showing forest cover worldwide",
                "tags": ["forest", "deforestation", "environment"],
                "thumbnail": "thumbnail.png",
                "access": "public",
                "num_views": 15432,
                "avg_rating": 4.7,
                "num_ratings": 23,
                "created": 1514764800000,
                "modified": 1672531200000,
                "portal_item_url": "https://www.arcgis.com/home/item.html?id=abc123def456",
                "service_url": "https://services.arcgis.com/.../FeatureServer", // For services
                "feature_server_url": "https://services.arcgis.com/.../FeatureServer" // For feature layers
            }
        ]
    },
    "type_breakdown": {
        "Web Map": 25,
        "Feature Service": 15,
        "Feature Layer": 10
    },
    "chat_summary": "Found 150 items matching 'forest' of type 'Web Map'. Top results: Global Forest Watch (Web Map), Forest Fire Risk (Feature Service), Protected Areas (Feature Layer)"
}
```

### `geocode(address: str)`
Geocodes an address and returns coordinates with metadata.

**Parameters:**
- `address` (str): The address string to geocode

**Returns:**
```json
{
    "success": true,
    "address": "Original address input",
    "formatted_address": "Standardized address from service",
    "coordinates": {
        "latitude": 37.4419,
        "longitude": -122.1430
    },
    "score": 95,
    "attributes": {},
    "raw_response": {}
}
```

### `reverse_geocode(latitude: float, longitude: float)`
Reverse geocodes coordinates to get address and location information.

**Parameters:**
- `latitude` (float): The latitude coordinate (e.g., 37.4419)
- `longitude` (float): The longitude coordinate (e.g., -122.1430)

**Returns:**
```json
{
    "success": true,
    "coordinates": {
        "latitude": 37.4219999,
        "longitude": -122.0840575
    },
    "formatted_address": "1600 Amphitheatre Parkway, Mountain View, CA 94043, USA",
    "address_components": {
        "street": "1600 Amphitheatre Parkway",
        "city": "Mountain View",
        "state": "CA",
        "postal_code": "94043",
        "country": "USA"
    },
    "location_type": "4326",
    "raw_response": {}
}
```

### `render_static_map_from_coordinates(latitude: float, longitude: float, zoom: int = 15, style: str = None)` 🆕
Renders a static map tile from coordinates as a binary Image object for direct display in chat UIs.

**Parameters:**
- `latitude` (float): Center latitude for the map
- `longitude` (float): Center longitude for the map  
- `zoom` (int): Zoom level (0-22, default: 15)
- `style` (str): Map style (optional, defaults to "navigation")

**Returns:**
Image object containing the static map tile as binary data, always returns Image even on errors.

### `render_static_map_from_location(location: str, zoom: int = None, style: str = None)` 🆕
Renders a static map from a location string with automatic zoom and style selection based on location type.

**Parameters:**
- `location` (str): Location string (address, place name, etc.)
- `zoom` (int): Optional zoom override (auto-determined from location type if not provided)  
- `style` (str): Optional style override (auto-determined from location type if not provided)

**Returns:**
Image object containing the static map tile as binary data.

**Auto-Detection:**
- Country-level → zoom 4, "world" style
- City-level → zoom 11, "navigation" style
- Address-level → zoom 16, "navigation" style

### `generate_static_map_from_coordinates(latitude: float, longitude: float, zoom: int = 15, include_image_data: bool = False)`
Generate a static map tile from coordinates using ArcGIS basemap tiles.

**Parameters:**
- `latitude` (float): Center latitude for the map
- `longitude` (float): Center longitude for the map  
- `zoom` (int): Zoom level (0-22, default: 15)
- `include_image_data` (bool): If True, return base64 encoded image data

**Returns:**
```json
{
    "success": true,
    "tile_coordinates": {
        "x": 5242,
        "y": 12666, 
        "z": 15
    },
    "center_coordinates": {
        "latitude": 40.7128,
        "longitude": -74.0060
    },
    "tile_url": "https://basemap.arcgis.com/arcgis/rest/services/World_Basemap_v2/MapServer/tile/15/12666/5242",
    "tile_size": "512x512",
    "format": "PNG",
    "map_context": {
        "service": "ArcGIS World Basemap v2",
        "projection": "Web Mercator (EPSG:3857)",
        "zoom_description": "Neighborhood",
        "coverage": "Global"
    }
}
```

### `generate_static_map_from_address(address: str, zoom: int = 15, include_image_data: bool = False)`
Generate a static map tile from an address using ArcGIS basemap tiles.

**Parameters:**
- `address` (str): Address or place name to map
- `zoom` (int): Zoom level (0-22, default: 15)
- `include_image_data` (bool): If True, return base64 encoded image data

**Returns:**
```json
{
    "success": true,
    "tile_coordinates": {
        "x": 5242,
        "y": 12666,
        "z": 15
    },
    "center_coordinates": {
        "latitude": 40.7128,
        "longitude": -74.0060
    },
    "tile_url": "https://basemap.arcgis.com/arcgis/rest/services/World_Basemap_v2/MapServer/tile/15/12666/5242",
    "tile_size": "512x512", 
    "format": "PNG",
    "map_context": {
        "service": "ArcGIS World Basemap v2",
        "projection": "Web Mercator (EPSG:3857)",
        "zoom_description": "Neighborhood",
        "coverage": "Global"
    },
    "geocoding": {
        "input_address": "Times Square, New York",
        "formatted_address": "Times Square, New York, NY, USA",
        "geocoding_score": 100
    }
}
```

### `generate_map_url(address: str, zoom_level: int = 15)`
Generates map URLs for displaying geocoded locations.

**Parameters:**
- `address` (str): The geocoded address to generate map for
- `zoom_level` (int): Map zoom level (default: 15)

**Returns:**
```json
{
    "success": true,
    "address": "input address",
    "map_urls": {
        "google_maps": "URL for Google Maps",
        "openstreetmap": "URL for OpenStreetMap", 
        "arcgis": "URL for ArcGIS",
        "coordinates": "lat,lon"
    },
    "embed_html": "HTML for embedding map"
}
```

### `display_location_on_map(address: str, include_html: bool = True, zoom_level: int = 15)`
Complete tool for displaying a geocoded location on a map in the chat UI.

**Parameters:**
- `address` (str): The address to display on map
- `include_html` (bool): Whether to include HTML embed code (default: True)
- `zoom_level` (int): Map zoom level (default: 15)

**Returns:**
Complete map display package including coordinates, URLs, embed HTML, and markdown formatting.

### `get_elevation_for_coordinates(latitude: float, longitude: float)`
Get elevation data for specific coordinates.

**Parameters:**
- `latitude` (float): The latitude coordinate (e.g., 37.4419)
- `longitude` (float): The longitude coordinate (e.g., -122.1430)

**Returns:**
```json
{
    "success": true,
    "coordinates": {
        "latitude": 37.4419,
        "longitude": -122.1430
    },
    "elevation": {
        "meters": 1416.25,
        "feet": 4647.31
    },
    "data_source": "ArcGIS Location Platform Elevation Service",
    "raw_response": {}
}
```

### `get_directions(origin: str, destination: str, travel_mode: str = "driving")`
Get directions and routing information between two locations.

**Parameters:**
- `origin` (str): The starting location (address or coordinates as "lat,lon")
- `destination` (str): The ending location (address or coordinates as "lat,lon")
- `travel_mode` (str): Transportation mode - "driving", "walking", or "trucking" (default: "driving")

**Returns:**
```json
{
    "success": true,
    "origin": "San Francisco, CA",
    "destination": "Oakland, CA",
    "travel_mode": "driving",
    "route_summary": {
        "total_time_minutes": 25.5,
        "total_distance_miles": 12.3,
        "total_time_formatted": "25m"
    },
    "directions": [
        {
            "instruction": "Head north on Main St",
            "distance": 0.5,
            "time": 2.1,
            "maneuver_type": "esriDMTStraight"
        }
    ],
    "route_geometry": {},
    "formatted_directions": "🗺️ **Driving Directions**...",
    "raw_response": {}
}
```

### `get_elevation_for_address(address: str)`
Get elevation data for an address by first geocoding it.

**Parameters:**
- `address` (str): The address string to get elevation for

**Returns:**
```json
{
    "success": true,
    "address": "input address",
    "formatted_address": "geocoded address",
    "coordinates": {
        "latitude": 37.4419,
        "longitude": -122.1430
    },
    "elevation": {
        "meters": 1416.25,
        "feet": 4647.31
    },
    "data_source": "ArcGIS Location Platform Elevation Service",
    "geocoding_score": 85
}
```

### `display_location_with_elevation(address: str, include_html: bool = True, zoom_level: int = 15)`
Complete tool for displaying a geocoded location with elevation data in the chat UI.

**Parameters:**
- `address` (str): The address to display on map with elevation
- `include_html` (bool): Whether to include HTML embed code (default: True)
- `zoom_level` (int): Map zoom level (default: 15)

**Returns:**
Complete display package including coordinates, elevation, map URLs, embed HTML, and markdown formatting with elevation information.
## Resources Available

### `location://{address}`
Get formatted location information for a geocoded address.

**Example:** `location://1600 Amphitheatre Parkway, Mountain View, CA`

### `reverse_geocode://{latitude},{longitude}`
Get address information for coordinates.

**Example:** `reverse_geocode://37.4219999,-122.0840575`

### `elevation://{latitude},{longitude}`
Get elevation information for coordinates.

**Example:** `elevation://37.4219999,-122.0840575`

### `elevation_address://{address}`
Get elevation information for an address.

**Example:** `elevation_address://Mount Washington, New Hampshire`

### `places://{location}`
Get places information near a location address.

**Example:** `places://Times Square, New York, NY`

### `places://{latitude},{longitude}`
Get places information near specific coordinates.

**Example:** `places://40.7589,-73.9851`

## Usage Examples

### Enhanced Map Rendering (NEW)
```python
# 🆕 Smart map rendering with auto-zoom and style detection
country_map = render_static_map_from_location("Germany")  # Auto: zoom 4, world style
city_map = render_static_map_from_location("Bonn, Germany")  # Auto: zoom 11, navigation style
address_map = render_static_map_from_location("1600 Pennsylvania Ave")  # Auto: zoom 16, navigation style

# Override auto-detection
custom_map = render_static_map_from_location("Paris, France", zoom=8, style="world")

# Enhanced coordinate rendering with custom style
map_image = render_static_map_from_coordinates(40.7128, -74.0060, zoom=15, style="navigation")
# Always returns Image object, even on errors
```

### Location Type Auto-Detection
```python
# The system automatically detects location granularity:

# Country-level: "Germany", "United States" 
# → zoom 4, "world" style, good for country boundaries

# City-level: "Berlin, Germany", "New York, NY"
# → zoom 11, "navigation" style, good for urban overviews  

# Address-level: "1600 Pennsylvania Ave", "Times Square"
# → zoom 16, "navigation" style, good for street-level detail
```

### Static Basemap Tiles
```python
# Generate static map tile from coordinates
tile_result = generate_static_map_from_coordinates(40.7128, -74.0060, zoom=12)
if tile_result["success"]:
    print(f"Tile URL: {tile_result['tile_url']}")
    print(f"Zoom level: {tile_result['map_context']['zoom_description']}")
    print(f"Tile coordinates: {tile_result['tile_coordinates']}")

# Generate static map tile from address
tile_result = generate_static_map_from_address("Eiffel Tower, Paris", zoom=16, include_image_data=True)
if tile_result["success"]:
    print(f"Address: {tile_result['geocoding']['formatted_address']}")
    print(f"Tile URL: {tile_result['tile_url']}")
    if "image_data" in tile_result:
        print("Base64 image data available for display")
```

### Basic Geocoding
```python
# Using the geocode tool
result = geocode("1600 Amphitheatre Parkway, Mountain View, CA")
print(f"Coordinates: {result['coordinates']['latitude']}, {result['coordinates']['longitude']}")
```

### Reverse Geocoding
```python
# Using the reverse_geocode tool
result = reverse_geocode(37.4219999, -122.0840575)
print(f"Address: {result['formatted_address']}")
print(f"City: {result['address_components']['city']}")
print(f"State: {result['address_components']['state']}")
```

### Elevation Lookup
```python
# Get elevation for coordinates
elevation = get_elevation_for_coordinates(36.5786, -118.2923)  # Mount Whitney
print(f"Elevation: {elevation['elevation']['meters']} m ({elevation['elevation']['feet']} ft)")

# Get elevation for an address
elevation = get_elevation_for_address("Mount Washington, New Hampshire")
print(f"Address: {elevation['formatted_address']}")
print(f"Elevation: {elevation['elevation']['meters']} m")
```

### Nearby Places Search
```python
# Find restaurants near a specific address
places_result = find_places("Times Square, New York, NY", category="restaurant", radius=500, max_results=5)
print(f"Found {places_result['results']['total_found']} restaurants")
for place in places_result['results']['places']:
    print(f"- {place['name']}: {place['address']} ({place['distance']}m away)")

# Display places on an interactive map
print(places_result['map_visualization']['search_area_html'])  # HTML for embedding

# Find any type of place near coordinates
all_places = find_places_by_coordinates(40.7589, -73.9851, radius=1000, max_results=20)
print(all_places['chat_summary'])  # Human-friendly summary
```

### Map Display in Chat UI
```python
# Generate map URLs for a geocoded address
map_data = generate_map_url("1600 Amphitheatre Parkway, Mountain View, CA", zoom_level=15)
print(f"Google Maps URL: {map_data['map_urls']['google_maps']}")

# Complete map display package (geocodes if needed)
display_package = display_location_on_map("1600 Amphitheatre Parkway, Mountain View, CA")
print(display_package['markdown_map'])  # Formatted for chat display
print(display_package['embed_html'])    # HTML for embedding in UI
```

### Location with Elevation Display
```python
# Complete display package with elevation data
elevation_display = display_location_with_elevation("Denver, Colorado")
print(elevation_display['markdown_map'])  # Includes elevation in markdown format
```

### Routing & Directions
```python
# Get driving directions between two locations
directions = get_directions("San Francisco, CA", "Oakland, CA", travel_mode="driving")
print(f"Travel time: {directions['route_summary']['total_time_formatted']}")
print(f"Distance: {directions['route_summary']['total_distance_miles']} miles")

# Display formatted directions in chat
print(directions['formatted_directions'])

# Get walking directions using coordinates
walking_dirs = get_directions("37.7749,-122.4194", "37.8049,-122.4194", travel_mode="walking")
if walking_dirs['success']:
    for i, step in enumerate(walking_dirs['directions'][:5], 1):
        print(f"{i}. {step['instruction']}")
```

## API Integration
The service uses ArcGIS Location Platform services for geocoding, elevation, routing, and places search. For production use:

### ArcGIS Location Platform
This service integrates with ArcGIS Location Platform for:
- **Geocoding Service**: World Geocoding Service for address resolution
- **Elevation Service**: Point Elevation service for terrain data  
- **Places Service**: Places API for nearby points of interest search
- **Routing Service**: World Route Service for directions and travel information
- **Static Basemap Tiles**: World Basemap v2 for static map tile imagery
- **API Key Management**: Automatic handling of API keys via environment variables

### Supported Place Categories
The places search supports category filtering with values like:
- `restaurant` - Restaurants and food establishments
- `gas_station` - Gas stations and fuel services  
- `park` - Parks and recreational areas
- `hotel` - Hotels and accommodations
- `hospital` - Hospitals and medical facilities
- `pharmacy` - Pharmacies and drug stores
- `bank` - Banks and financial services
- `shopping_mall` - Shopping centers and malls
- `school` - Schools and educational institutions
- `tourist_attraction` - Tourist attractions and landmarks

### Authentication
API authentication is handled through the `ArcGISApiKeyManager` which looks for:
- Environment variable: `ARCGIS_API_KEY`
- Falls back to free tier services when no API key is provided
- API key can be explicitly passed to functions for custom authentication

1. Obtain an API key from [ArcGIS Location Platform](https://location.arcgis.com/)
2. Pass the API key to the geocoding, elevation, routing, and places functions
3. Monitor usage to stay within API limits

### Supported APIs:
- **Geocoding**: ArcGIS World Geocoding Service
- **Elevation**: ArcGIS Location Platform Elevation Services (Point Elevation)
- **Routing**: ArcGIS World Route Service with support for driving, walking, and trucking modes
- **Places**: ArcGIS Places Service for point-of-interest searches
- **Static Basemap**: ArcGIS World Basemap v2 tile service with zoom levels 0-22

## Error Handling
The service gracefully handles:
- Network connectivity issues
- Invalid addresses and coordinates
- API service unavailability
- Missing or malformed responses
- Elevation data unavailability
- Routing failures between locations

Failed requests return:
```json
{
    "success": false,
    "address": "input address",
    "error": "Error description",
    "coordinates": null
}
```

Failed routing attempts return:
```json
{
    "success": false,
    "origin": "input origin",
    "destination": "input destination",
    "travel_mode": "driving",
    "error": "Error description"
}
```

## Testing
Run the test suite to verify all functionality:
```bash
python test_geocoding.py
python test_basemap_tiles.py
```

The test suite covers:
- Geocoding and reverse geocoding functions
- Elevation data retrieval
- Map display and URL generation
- Static basemap tile generation and coordinate conversion
- Routing and directions with different travel modes
- Places search functionality
- Error handling for all services
- Chat UI integration and formatting

## Server Start
Start the MCP server:
```bash
python src/mcp/server/location/location_server.py
```

The server will be available at `http://127.0.0.1:8000` with all location, elevation, routing, and places tools accessible via MCP protocol.

# MCP Location Server Implementation Documentation

## Overview

The MCP Location Server provides a robust and modular framework for location-based services. This document explains the current architecture and its components, detailing how they work together to deliver functionality.

## Architecture

### Components

1. **LocationServer Class** (`location_server_class.py`)
   - Encapsulates server registration logic for reusability.
   - Manages the server lifecycle, including creation, startup, and shutdown.
   - Validates configurations and injects dependencies.
   - Provides comprehensive logging and error handling.

2. **Server Configuration** (`server_config.py`)
   - Centralized configuration management for the server.
   - Supports custom server settings and capability validation.
   - Ensures a clear separation between configuration and business logic.

3. **Entry Point** (`server_main.py`)
   - Acts as the main entry point for starting the server.
   - Demonstrates clean dependency wiring and minimal startup code.
   - Simplifies customization for different deployment scenarios.

4. **Location Services** (`location_server.py`)
   - Implements core location-based functionalities, such as geocoding, map rendering, and basemap tile retrieval.
   - Integrates with the `LocationServer` class for server registration.
   - Provides tools for generating static maps, handling bounding boxes, and supporting multiple basemap styles.

## Key Features

- **Modularity**: The architecture separates server setup from business logic, making it easier to maintain and extend.
- **Reusability**: The `LocationServer` class can be reused across different projects and contexts.
- **Testability**: Comprehensive unit tests ensure reliability and allow for mocking dependencies during testing.
- **Extensibility**: The design allows for easy addition of new features, configuration options, and capabilities.
- **Error Handling**: Robust error handling mechanisms ensure stability and provide detailed logs for debugging.

## Usage

- **Starting the Server**: Use `server_main.py` to start the server with the desired configuration.
- **Customizing Configuration**: Modify `server_config.py` to adjust server settings and capabilities.
- **Adding New Features**: Extend `location_server.py` or create new modules to add functionality while leveraging the existing framework.

## Unit Testing

### Running Unit Tests

To run the unit tests for the MCP Location Server, use the following command:

```bash
python -m unittest discover -s src/mcp -p "test_*.py"
```

This command discovers and runs all test files matching the pattern `test_*.py` in the `src/mcp` directory.

### Test Coverage

The unit tests cover the following cases:

1. **Geocoding Functionality**
   - Validates geocoding results for various input addresses.
   - Tests error handling for invalid or empty addresses.

2. **Static Basemap Tile Retrieval**
   - Ensures correct tile URLs are generated for given coordinates and zoom levels.
   - Tests handling of invalid coordinates and zoom levels.

3. **Bounding Box Tile Retrieval**
   - Verifies that the correct tiles are returned for a given bounding box and zoom level.
   - Tests edge cases, such as bounding boxes crossing the International Date Line.

4. **Map Rendering**
   - Validates the rendering of static maps for different styles and zoom levels.
   - Ensures compatibility with various basemap styles and configurations.

5. **Configuration Management**
   - Tests loading and validation of server configurations.
   - Ensures proper error handling for invalid configurations.

6. **Server Lifecycle Management**
   - Verifies the creation, startup, and shutdown of the `LocationServer` class.
   - Tests logging and error handling during the server lifecycle.

These tests ensure the reliability and robustness of the MCP Location Server's implementation.