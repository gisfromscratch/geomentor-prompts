# Location Services Documentation

## Overview
The Location MCP Server includes forward and reverse geocoding functionality, as well as elevation data services using ArcGIS Location Platform services to convert between addresses and geographic coordinates, and to retrieve elevation information.

## Features
- **Address Geocoding**: Convert text addresses to latitude/longitude coordinates
- **Reverse Geocoding**: Convert latitude/longitude coordinates to readable addresses
- **Elevation Services**: Get elevation data for coordinates or addresses
- **Metadata Storage**: Store geocoded and elevation results for efficient retrieval
- **Error Handling**: Robust error handling for failed geocoding and elevation attempts
- **Resource Endpoints**: Access location and elevation data through MCP resources
- **Chat UI Integration**: Display maps and elevation data in chat interfaces

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

## API Integration
The service uses ArcGIS Location Platform services for both geocoding and elevation. For production use:

1. Obtain an API key from [ArcGIS Location Platform](https://location.arcgis.com/)
2. Pass the API key to the geocoding and elevation functions
3. Monitor usage to stay within API limits

**APIs Used:**
- **Geocoding**: ArcGIS Location Platform Geocoding Services
- **Elevation**: ArcGIS Location Platform Elevation Services (Point Elevation)

## Error Handling
The service gracefully handles:
- Network connectivity issues
- Invalid addresses or coordinates
- API service unavailability
- Missing or malformed responses
- Elevation data unavailability

Failed requests return:
```json
{
    "success": false,
    "address": "input address",
    "error": "Error description",
    "coordinates": null
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
- Error handling for all services
- Map display functionality
- Chat UI integration

## Server Start
Start the MCP server:
```bash
python src/mcp/server/location/location_server.py
```

The server will be available at `http://127.0.0.1:8000` with all location and elevation tools accessible via MCP protocol.