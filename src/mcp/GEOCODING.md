# Location Services Documentation

## Overview
The Location MCP Server includes geocoding, reverse geocoding, elevation data services, map display, routing functionality, and nearby places search using ArcGIS Location Platform services to provide comprehensive location-based services including coordinate conversion, elevation information, and point-of-interest discovery.

## Features
- **Address Geocoding**: Convert text addresses to latitude/longitude coordinates
- **Reverse Geocoding**: Convert latitude/longitude coordinates to readable addresses
- **Elevation Services**: Get elevation data for coordinates or addresses
- **Routing & Directions**: Get turn-by-turn directions between locations with travel time and distance
- **Map Display**: Generate map URLs and embed HTML for various mapping services
- **Interactive Maps**: Generate embeddable maps for chat UI display
- **Nearby Places Search**: Find places of interest around a location with category filtering
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
```

The test suite covers:
- Geocoding and reverse geocoding functions
- Elevation data retrieval
- Map display and URL generation
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