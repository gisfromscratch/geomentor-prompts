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