# Elevation Services

## Overview
The Elevation service provides terrain elevation data for geographic coordinates and addresses using the ArcGIS Location Platform Elevation Services. This service is essential for applications requiring topographic information, altitude calculations, and terrain analysis.

## Available Tools

### `get_elevation_for_coordinates(latitude: float, longitude: float)`
Get elevation data for specific geographic coordinates.

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
Get elevation data for an address by first geocoding the location.

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
Complete tool for displaying a geocoded location with elevation data in chat UI.

**Parameters:**
- `address` (str): The address to display with elevation information
- `include_html` (bool): Whether to include HTML embed code (default: True)
- `zoom_level` (int): Map zoom level (default: 15)

**Returns:**
Complete display package including coordinates, elevation, map URLs, embed HTML, and markdown formatting with elevation information integrated for chat interfaces.

## Resource Endpoints

### `elevation://{latitude},{longitude}`
Direct access to elevation information for coordinates.

**Example:** `elevation://37.4219999,-122.0840575`

**Returns:** Formatted elevation information including both metric and imperial units

### `elevation_address://{address}`
Direct access to elevation information for an address.

**Example:** `elevation_address://Mount Washington, New Hampshire`

**Returns:** Formatted elevation information with geocoded address details

## Usage Examples

### Basic Elevation Lookup
```python
# Get elevation for specific coordinates
elevation = get_elevation_for_coordinates(36.5786, -118.2923)  # Mount Whitney
if elevation["success"]:
    elev_data = elevation["elevation"]
    print(f"Elevation: {elev_data['meters']} m ({elev_data['feet']} ft)")
    print(f"Data source: {elevation['data_source']}")
```

### Elevation for Address
```python
# Get elevation for a named location
elevation = get_elevation_for_address("Mount Washington, New Hampshire")
if elevation["success"]:
    print(f"Location: {elevation['formatted_address']}")
    print(f"Coordinates: {elevation['coordinates']['latitude']}, {elevation['coordinates']['longitude']}")
    print(f"Elevation: {elevation['elevation']['meters']} m")
    print(f"Geocoding accuracy: {elevation['geocoding_score']}/100")
```

### Elevation with Map Display
```python
# Display location with elevation in chat UI
display_package = display_location_with_elevation("Denver, Colorado")
if display_package["success"]:
    print(display_package['markdown_map'])  # Formatted for chat display
    print(display_package['embed_html'])    # HTML for embedding in UI
```

### Batch Elevation Processing
```python
# Process multiple locations
locations = [
    {"name": "Mount Whitney", "coords": (36.5786, -118.2923)},
    {"name": "Death Valley", "coords": (36.5054, -117.0794)},
    {"name": "Denver", "coords": (39.7392, -104.9903)}
]

for location in locations:
    lat, lon = location["coords"]
    elevation = get_elevation_for_coordinates(lat, lon)
    if elevation["success"]:
        elev_m = elevation["elevation"]["meters"]
        print(f"{location['name']}: {elev_m} meters")
```

## API Integration

### ArcGIS Location Platform Elevation Services
This service integrates with the ArcGIS Point Elevation service which provides:
- Global elevation coverage
- High-resolution terrain data
- Seamless data source integration
- Reliable elevation measurements

### Data Sources
The elevation service uses multiple high-quality data sources:
- **USGS 3DEP**: High-resolution US elevation data
- **SRTM**: Global 30-meter resolution data
- **ASTER GDEM**: Additional global coverage
- **Local DEMs**: Regional high-accuracy datasets

### Authentication
```python
# Using environment variable (recommended)
export ARCGIS_API_KEY="your_api_key_here"

# Or pass API key directly
elevation = get_elevation_for_coordinates(lat, lon, api_key="your_api_key")
```

## Response Format Details

### Success Response Structure
- `success`: Boolean indicating operation success
- `coordinates`: Input coordinates object
- `elevation`: Elevation data in meters and feet
- `data_source`: Attribution for elevation data
- `raw_response`: Complete API response

### Address-Based Response
When using address input, additional fields include:
- `address`: Original input address
- `formatted_address`: Standardized geocoded address
- `geocoding_score`: Accuracy of address geocoding (0-100)

### Error Response Structure
```json
{
    "success": false,
    "coordinates": {"latitude": 37.4419, "longitude": -122.1430},
    "error": "Elevation data unavailable for this location",
    "elevation": null
}
```

## Error Handling

### Common Scenarios
The elevation service handles various error conditions:
- **No elevation data available**: Some coordinates may not have elevation coverage
- **Network connectivity issues**: Graceful handling of connection problems
- **Invalid coordinates**: Validation of latitude/longitude ranges
- **Service unavailability**: Fallback error messages when API is down

### Best Practices
```python
# Always check success status
elevation = get_elevation_for_coordinates(lat, lon)
if elevation["success"]:
    # Use elevation data
    meters = elevation["elevation"]["meters"]
    feet = elevation["elevation"]["feet"]
else:
    # Handle error appropriately
    print(f"Elevation lookup failed: {elevation['error']}")
```

## Accuracy and Limitations

### Data Accuracy
- **Vertical accuracy**: Typically ±1-10 meters depending on data source
- **Horizontal resolution**: 10-30 meters for most global areas
- **Coverage**: Global coverage with varying resolution
- **Data age**: Elevation data represents terrain, not structures

### Use Case Considerations
- **Suitable for**: Terrain analysis, hiking apps, aviation planning
- **Not suitable for**: Building heights, real-time water levels
- **Ocean areas**: May return sea level (0m) or null values
- **Polar regions**: Limited accuracy in extreme latitudes

## Performance Optimization

### Caching Strategies
```python
# Cache elevation results for frequently accessed coordinates
elevation_cache = {}

def get_cached_elevation(lat, lon):
    key = f"{lat:.4f},{lon:.4f}"
    if key not in elevation_cache:
        elevation_cache[key] = get_elevation_for_coordinates(lat, lon)
    return elevation_cache[key]
```

### Batch Processing
- Group nearby coordinates for efficient processing
- Use appropriate precision for coordinate keys
- Consider rate limits when processing large datasets

## Testing

The elevation service includes comprehensive tests:
```bash
# Run elevation-specific tests
python src/mcp/test_geocoding.py  # Includes elevation tests
```

Test coverage includes:
- Valid coordinate elevation lookup
- Invalid coordinate handling
- Address-based elevation requests
- Error response validation
- Data source attribution
- Unit conversion accuracy