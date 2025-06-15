# Geocoding Services

## Overview
The Geocoding service provides address-to-coordinate conversion (geocoding) and coordinate-to-address conversion (reverse geocoding) using the ArcGIS World Geocoding Service. This service is essential for converting human-readable addresses into geographic coordinates and vice versa.

## Available Tools

### `geocode(address: str)`
Converts an address string to geographic coordinates with metadata.

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
Converts geographic coordinates to address and location information.

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

## Resource Endpoints

### `location://{address}`
Direct access to formatted location information for a geocoded address.

**Example:** `location://1600 Amphitheatre Parkway, Mountain View, CA`

**Returns:** Formatted location information ready for display

### `reverse_geocode://{latitude},{longitude}`
Direct access to address information for coordinates.

**Example:** `reverse_geocode://37.4219999,-122.0840575`

**Returns:** Formatted address information for the coordinates

## Usage Examples

### Basic Geocoding
```python
# Geocode a standard address
result = geocode("1600 Amphitheatre Parkway, Mountain View, CA")
if result["success"]:
    coords = result["coordinates"]
    print(f"Latitude: {coords['latitude']}")
    print(f"Longitude: {coords['longitude']}")
    print(f"Formatted Address: {result['formatted_address']}")
    print(f"Accuracy Score: {result['score']}/100")
```

### Reverse Geocoding
```python
# Convert coordinates to address
result = reverse_geocode(37.4219999, -122.0840575)
if result["success"]:
    print(f"Address: {result['formatted_address']}")
    
    # Access address components
    components = result['address_components']
    print(f"City: {components['city']}")
    print(f"State: {components['state']}")
    print(f"Postal Code: {components['postal_code']}")
    print(f"Country: {components['country']}")
```

### Error Handling
```python
# Handle geocoding failures gracefully
result = geocode("Invalid Address XYZ123")
if not result["success"]:
    print(f"Geocoding failed: {result['error']}")
    print(f"Original input: {result['address']}")
```

## API Integration

### ArcGIS World Geocoding Service
This service integrates with the ArcGIS World Geocoding Service which provides:
- Global address coverage
- High-accuracy coordinate resolution
- Standardized address formatting
- Confidence scoring for results

### Authentication
```python
# Using environment variable (recommended)
export ARCGIS_API_KEY="your_api_key_here"

# Or pass API key directly
result = geocode("123 Main St", api_key="your_api_key")
```

### Rate Limits and Quotas
- Free tier: Limited requests per month
- Paid tiers: Higher quotas and additional features
- Monitor usage through ArcGIS Location Platform dashboard

## Response Format Details

### Success Response Structure
- `success`: Boolean indicating operation success
- `address`: Original input address
- `formatted_address`: Standardized address from the service
- `coordinates`: Latitude and longitude object
- `score`: Accuracy score (0-100, higher is better)
- `attributes`: Additional metadata from the service
- `raw_response`: Complete API response for advanced use

### Error Response Structure
```json
{
    "success": false,
    "address": "input address",
    "error": "Error description",
    "coordinates": null
}
```

## Best Practices

### Input Formatting
- Include as much address detail as possible
- Use standard address format for your region
- Include postal codes when available
- Specify country for international addresses

### Result Validation
- Check the `success` field before using results
- Consider the `score` field for accuracy assessment
- Scores above 80 are generally reliable
- Scores below 50 may need manual verification

### Performance Optimization
- Cache geocoding results for repeated addresses
- Batch process multiple addresses when possible
- Use appropriate error handling for network issues
- Store coordinates for frequently used addresses

## Testing

The geocoding service includes comprehensive tests:
```bash
# Run geocoding-specific tests
python src/mcp/test_geocoding.py
```

Test coverage includes:
- Valid address geocoding
- Invalid address handling
- Coordinate validation
- Network error scenarios
- API response parsing
- Error message formatting