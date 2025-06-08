# Geocoding Service Documentation

## Overview
The Location MCP Server now includes geocoding functionality using ArcGIS Location Platform Geocoding Services to convert user-entered addresses into geographic coordinates.

## Features
- **Address Geocoding**: Convert text addresses to latitude/longitude coordinates
- **Metadata Storage**: Store geocoded results for efficient retrieval
- **Error Handling**: Robust error handling for failed geocoding attempts
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

### `get_geocoded_metadata(address: Optional[str])`
Retrieves stored geocoded metadata.

**Parameters:**
- `address` (str, optional): Specific address to retrieve. If None, returns all stored data

**Returns:**
- If address specified: Geocoded data for that address
- If no address: Summary of all geocoded data

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

## Resources Available

### `location://{address}`
Get formatted location information for a geocoded address.

**Example:** `location://1600 Amphitheatre Parkway, Mountain View, CA`

## Usage Examples

### Basic Geocoding
```python
# Using the geocode tool
result = geocode("1600 Amphitheatre Parkway, Mountain View, CA")
print(f"Coordinates: {result['coordinates']['latitude']}, {result['coordinates']['longitude']}")
```

### Retrieving Stored Data
```python
# Get specific address metadata
metadata = get_geocoded_metadata("1600 Amphitheatre Parkway, Mountain View, CA")

# Get all stored geocoded data
all_data = get_geocoded_metadata()
print(f"Total geocoded addresses: {all_data['total_geocoded']}")
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

## API Integration
The service uses ArcGIS Location Platform Geocoding Services. For production use:

1. Obtain an API key from [ArcGIS Developers](https://developers.arcgis.com/)
2. Pass the API key to the geocoding function
3. Monitor usage to stay within API limits

## Error Handling
The service gracefully handles:
- Network connectivity issues
- Invalid addresses
- API service unavailability
- Missing or malformed responses

Failed geocoding attempts return:
```json
{
    "success": false,
    "address": "input address",
    "error": "Error description",
    "coordinates": null
}
```

## Testing
Run the test suite to verify functionality:
```bash
python test_geocoding.py
```

## Server Start
Start the MCP server:
```bash
python src/mcp/server/location/location_server.py
```

The server will be available at `http://127.0.0.1:8000`