# Location Services Documentation

## Overview
The Location MCP Server includes geocoding, reverse geocoding, map display, and routing functionality using ArcGIS Location Platform services to provide comprehensive location-based services.

## Features
- **Address Geocoding**: Convert text addresses to latitude/longitude coordinates
- **Reverse Geocoding**: Convert latitude/longitude coordinates to readable addresses
- **Routing & Directions**: Get turn-by-turn directions between locations with travel time and distance
- **Map Display**: Generate map URLs and embed HTML for various mapping services
- **Metadata Storage**: Store geocoded and routing results for efficient retrieval
- **Error Handling**: Robust error handling for failed requests
- **Resource Endpoints**: Access location data through MCP resources

## Tools Available

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

## Resources Available

### `location://{address}`
Get formatted location information for a geocoded address.

**Example:** `location://1600 Amphitheatre Parkway, Mountain View, CA`

### `reverse_geocode://{latitude},{longitude}`
Get address information for coordinates.

**Example:** `reverse_geocode://37.4219999,-122.0840575`

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
The service uses ArcGIS Location Platform services for geocoding and routing. For production use:

1. Obtain an API key from [ArcGIS Location Platform](https://location.arcgis.com/)
2. Pass the API key to the geocoding and routing functions
3. Monitor usage to stay within API limits

### Supported APIs:
- **Geocoding**: ArcGIS World Geocoding Service
- **Routing**: ArcGIS World Route Service with support for driving, walking, and trucking modes

## Error Handling
The service gracefully handles:
- Network connectivity issues
- Invalid addresses and coordinates
- API service unavailability
- Missing or malformed responses
- Routing failures between locations

Failed geocoding attempts return:
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
Run the test suite to verify functionality:
```bash
python test_geocoding.py
```

The test suite validates:
- Geocoding and reverse geocoding functionality
- Map display and URL generation
- Routing and directions with different travel modes
- Error handling for all services
- Chat UI formatting for directions

## Server Start
Start the MCP server:
```bash
python src/mcp/server/location/location_server.py
```

The server will be available at `http://127.0.0.1:8000`