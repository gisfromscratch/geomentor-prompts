# Location MCP Server

## Design Principles

The Location MCP Server provides comprehensive location-based services of ArcGIS Location Platform through a unified Model Context Protocol (MCP) interface. It follows these core design principles:

### 🎯 **Comprehensive Location Intelligence**
The Location MCP Server includes geocoding, reverse geocoding, elevation data services, map display, routing functionality, and nearby places search using ArcGIS Location Platform services to provide comprehensive location-based services including coordinate conversion, elevation information, and point-of-interest discovery.

### 🏗️ **Modular Service Architecture**
The server is built with distinct, focused services that can be used independently or combined:

- **[Geocoding Services](./geocoding.md)** - Address-to-coordinate conversion and reverse geocoding
- **[Elevation Services](./elevation.md)** - Terrain elevation data for coordinates and addresses  
- **[Routing Services](./routing.md)** - Turn-by-turn directions and travel optimization
- **[Places Services](./places.md)** - Point-of-interest discovery and nearby search
- **[Map Visualization](./maps.md)** - Interactive maps and embedding for chat interfaces

### 🔌 **MCP Protocol Integration**
Built on the Model Context Protocol standard, providing:
- **Tools**: Interactive functions for location operations
- **Resources**: Direct access to location data through URI schemes
- **Standardized Interface**: Consistent API patterns across all services

### 🛡️ **Robust Error Handling**
Graceful handling of common scenarios:
- Network connectivity issues
- Invalid addresses and coordinates
- API service unavailability
- Missing or malformed responses
- Service-specific failures (elevation, routing, etc.)

### 🚀 **Developer Experience Focus**
Designed for ease of integration:
- Clear, consistent API responses
- Comprehensive error messages
- Chat UI-ready formatted outputs
- HTML embeds for maps and visualizations
- Markdown-formatted responses for documentation

### 🌐 **Multi-Platform Map Support**
Generate URLs and embeds for multiple mapping services:
- ArcGIS Online
- Google Maps
- OpenStreetMap
- Coordinate-based references

### 📊 **Rich Metadata and Context**
Each response includes:
- Success/failure status
- Accuracy scores and confidence levels
- Data source attribution
- Raw API responses for advanced use
- Chat-friendly summaries

## Quick Start

### Installation
```bash
# Start the Location MCP Server
python src/mcp/server/location/location_server.py
```

The server will be available at `http://127.0.0.1:8000` with all location services accessible via MCP protocol.

### Authentication
Configure your ArcGIS Location Platform API key:
```bash
export ARCGIS_API_KEY="your_api_key_here"
```

Or pass the API key directly to functions for custom authentication.

### Basic Usage Examples

**Geocode an address:**
```python
result = geocode("1600 Amphitheatre Parkway, Mountain View, CA")
print(f"Coordinates: {result['coordinates']['latitude']}, {result['coordinates']['longitude']}")
```

**Find nearby restaurants:**
```python
places = find_places("Times Square, NYC", category="restaurant", radius=500)
print(f"Found {places['results']['total_found']} restaurants")
```

**Get driving directions:**
```python
directions = get_directions("San Francisco, CA", "Oakland, CA", travel_mode="driving")
print(f"Travel time: {directions['route_summary']['total_time_formatted']}")
```

## Architecture Overview

### Service Integration
All services integrate seamlessly with the ArcGIS Location Platform:
- **World Geocoding Service** for address resolution
- **Point Elevation Service** for terrain data
- **World Route Service** for directions and travel information  
- **Places API** for point-of-interest searches

### MCP Resource Endpoints
Direct access to location data through standardized URI schemes:
- `location://{address}` - Geocoded location information
- `elevation://{lat},{lon}` - Elevation data for coordinates
- `places://{location}` - Nearby places search results

### Testing and Validation
Comprehensive test suite covering:
- All core service functionality
- Error handling scenarios
- Chat UI integration
- Performance considerations

## Service Documentation

- **[Geocoding Services](./geocoding.md)** - Convert addresses to coordinates and vice versa
- **[Elevation Services](./elevation.md)** - Get terrain elevation data
- **[Routing Services](./routing.md)** - Calculate routes and directions
- **[Places Services](./places.md)** - Discover nearby points of interest
- **[Map Visualization](./maps.md)** - Display and embed interactive maps
