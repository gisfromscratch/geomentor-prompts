# Map Visualization Services

## Overview
The Map Visualization service provides interactive map generation, URL creation, embed HTML for displaying locations, routes, and places in chat interfaces and web applications, plus **static basemap tile generation** from ArcGIS Location Platform. This service integrates with multiple mapping platforms to provide comprehensive map display capabilities including real map imagery through tile services.

## Available Tools

### `render_static_map_from_coordinates(latitude: float, longitude: float, zoom: int = 15, style: str = None)`
Renders a static map tile from coordinates as a binary Image object for direct display in chat UIs.

**Parameters:**
- `latitude` (float): Center latitude for the map
- `longitude` (float): Center longitude for the map  
- `zoom` (int): Zoom level (0-22, default: 15)
- `style` (str): Map style (optional, defaults to "navigation")

**Returns:**
Image object containing the static map tile as binary data, ready for chat UI display.

**Example:**
```python
# Basic usage
map_image = render_static_map_from_coordinates(40.7128, -74.0060)

# With custom zoom and style
map_image = render_static_map_from_coordinates(40.7128, -74.0060, zoom=12, style="world")
```

### `render_static_map_from_location(location: str, zoom: int = None, style: str = None)` 
⭐ **NEW** - Renders a static map from a location string with automatic zoom and style selection.

**Parameters:**
- `location` (str): Location string (address, place name, etc.)
- `zoom` (int): Optional zoom override (auto-determined from location type if not provided)
- `style` (str): Optional style override (auto-determined from location type if not provided)

**Returns:**
Image object containing the static map tile as binary data.

**Auto-Detection Features:**
- **Country-level locations** (e.g., "Germany") → zoom 4, "world" style
- **City/community locations** (e.g., "Bonn, Germany") → zoom 11, "navigation" style  
- **Address-level locations** (e.g., "1600 Pennsylvania Ave") → zoom 16, "navigation" style

**Examples:**
```python
# Country view - auto zoom 4, world style
country_map = render_static_map_from_location("Germany")

# City view - auto zoom 11, navigation style  
city_map = render_static_map_from_location("Bonn, Germany")

# Address view - auto zoom 16, navigation style
address_map = render_static_map_from_location("1600 Pennsylvania Ave NW, Washington, DC")

# Override auto-detection
custom_map = render_static_map_from_location("Paris, France", zoom=8, style="world")
```

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
    "tile_coordinates": {"x": 5242, "y": 12666, "z": 15},
    "center_coordinates": {"latitude": 40.7128, "longitude": -74.0060},
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
Includes all fields from `generate_static_map_from_coordinates` plus geocoding information.

### `generate_map_url(address: str, zoom_level: int = 15)`
Generate map URLs for displaying geocoded locations across multiple mapping services.

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
Complete tool for displaying a geocoded location on a map in chat UI with rich formatting.

**Parameters:**
- `address` (str): The address to display on map
- `include_html` (bool): Whether to include HTML embed code (default: True)
- `zoom_level` (int): Map zoom level (default: 15)

**Returns:**
```json
{
    "success": true,
    "formatted_address": "Geocoded address",
    "coordinates": {"latitude": 37.4419, "longitude": -122.1430},
    "map_urls": {
        "google_maps": "https://www.google.com/maps?q=37.4419,-122.1430&z=15",
        "openstreetmap": "https://www.openstreetmap.org/?mlat=37.4419&mlon=-122.1430&zoom=15",
        "arcgis": "https://www.arcgis.com/home/webmap/viewer.html?center=-122.1430,37.4419&level=15"
    },
    "geocoding_score": 95,
    "embed_html": "HTML for embedding map",
    "markdown_map": "📍 **Address**\n\n🗺️ [View on Google Maps](URL)\n📐 Coordinates: `37.4419, -122.1430`\n🎯 Accuracy Score: 95/100"
}
```

### Map Embed HTML Generation
The service automatically generates embeddable HTML for chat interfaces and web applications.

## Supported Mapping Platforms

### Google Maps
- **URL Format**: `https://www.google.com/maps?q={lat},{lon}&z={zoom}`
- **Features**: Street view, satellite imagery, traffic data
- **Best for**: General purpose mapping, familiar interface

### OpenStreetMap
- **URL Format**: `https://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom={zoom}`
- **Features**: Open-source mapping, detailed coverage
- **Best for**: Open-source applications, custom styling

### ArcGIS Online
- **URL Format**: `https://www.arcgis.com/home/webmap/viewer.html?center={lon},{lat}&level={zoom}`
- **Features**: Professional GIS capabilities, advanced analysis
- **Best for**: Professional applications, spatial analysis

## Usage Examples

### Static Basemap Tiles
```python
# Generate static map tile from coordinates
tile_result = generate_static_map_from_coordinates(40.7128, -74.0060, zoom=15)
if tile_result["success"]:
    print(f"Tile URL: {tile_result['tile_url']}")
    print(f"Tile coordinates: x={tile_result['tile_coordinates']['x']}, y={tile_result['tile_coordinates']['y']}")
    print(f"Zoom description: {tile_result['map_context']['zoom_description']}")

# Generate static map with image data
tile_with_image = generate_static_map_from_coordinates(37.7749, -122.4194, zoom=12, include_image_data=True)
if tile_with_image["success"] and "image_data" in tile_with_image:
    print("PNG image data available as base64")
    # Can be used as: <img src="data:image/png;base64,{image_data}">

# Generate static map from address
address_tile = generate_static_map_from_address("Eiffel Tower, Paris", zoom=16)
if address_tile["success"]:
    print(f"Address: {address_tile['geocoding']['formatted_address']}")
    print(f"Map tile: {address_tile['tile_url']}")
    print(f"Geocoding score: {address_tile['geocoding']['geocoding_score']}")
```

### Basic Map URL Generation
```python
# Generate map URLs for a location
map_data = generate_map_url("1600 Amphitheatre Parkway, Mountain View, CA", zoom_level=15)
if map_data["success"]:
    urls = map_data["map_urls"]
    print(f"Google Maps: {urls['google_maps']}")
    print(f"OpenStreetMap: {urls['openstreetmap']}")
    print(f"ArcGIS: {urls['arcgis']}")
    print(f"Coordinates: {urls['coordinates']}")
```

### Complete Map Display Package
```python
# Generate complete map display for chat UI
display_package = display_location_on_map("Times Square, New York, NY")
if display_package["success"]:
    # Use markdown format for chat display
    print(display_package['markdown_map'])
    
    # Embed HTML in web interface
    html_content = display_package['embed_html']
    # Insert html_content into your web page
    
    # Access individual map URLs
    google_url = display_package['map_urls']['google_maps']
```

### Custom Zoom Levels
```python
# Different zoom levels for different use cases
city_view = display_location_on_map("San Francisco, CA", zoom_level=10)  # City overview
street_view = display_location_on_map("123 Main St, San Francisco, CA", zoom_level=18)  # Street level
region_view = display_location_on_map("California, USA", zoom_level=6)  # State/region
```

### Map Display with Places
```python
# Generate map showing places search results
places_result = find_places("Downtown Seattle", category="restaurant", radius=500)
if places_result["success"]:
    # The places result includes map visualization
    places_map_html = places_result['map_visualization']['search_area_html']
    print(places_map_html)  # Embeddable map showing restaurant locations
```

### Error Handling
```python
# Handle geocoding failures in map generation
map_data = generate_map_url("Invalid Address XYZ123")
if not map_data["success"]:
    print(f"Map generation failed: {map_data['error']}")
else:
    print("Map URLs generated successfully")
```

## HTML Embed Features

### Basic Map Embed
The generated HTML includes:
- Responsive iframe containers
- Multiple map service options
- Fallback coordinate display
- Mobile-friendly design

### Example HTML Output
```html
<div class="map-container" style="width: 100%; max-width: 600px; margin: 10px 0;">
    <div style="margin-bottom: 10px;">
        <strong>📍 Location:</strong> 1600 Amphitheatre Parkway, Mountain View, CA
    </div>
    <div style="margin-bottom: 10px;">
        <strong>🗺️ View on:</strong>
        <a href="https://www.google.com/maps?q=37.4419,-122.1430&z=15" target="_blank">Google Maps</a> |
        <a href="https://www.openstreetmap.org/?mlat=37.4419&mlon=-122.1430&zoom=15" target="_blank">OpenStreetMap</a> |
        <a href="https://www.arcgis.com/home/webmap/viewer.html?center=-122.1430,37.4419&level=15" target="_blank">ArcGIS</a>
    </div>
    <iframe src="https://www.google.com/maps/embed?pb=..." width="100%" height="300" frameborder="0" style="border:0" allowfullscreen></iframe>
</div>
```

### Places Map HTML
For places searches, the HTML includes:
- Markers for each found place
- Info windows with place details
- Search radius visualization
- Interactive map controls

## Chat Interface Integration

### Markdown Format
The service provides chat-ready markdown formatting:
```markdown
📍 **1600 Amphitheatre Parkway, Mountain View, CA**

🗺️ [View on Google Maps](https://www.google.com/maps?q=37.4419,-122.1430&z=15)
📐 Coordinates: `37.4419, -122.1430`
🎯 Accuracy Score: 95/100
```

### Rich Display Components
- **Location emoji** (📍): Visual location indicator
- **Map emoji** (🗺️): Map service links
- **Coordinates emoji** (📐): Precise coordinates
- **Target emoji** (🎯): Accuracy indicator

### Responsive Design
- **Mobile-friendly**: Maps scale appropriately on mobile devices
- **Loading states**: Graceful handling of slow map loading
- **Fallback content**: Coordinate display when maps fail to load

## Automatic Zoom and Style Detection

### Location Type → Zoom/Style Mapping

The `render_static_map_from_location` function automatically determines the appropriate zoom level and map style based on the geocoded location type:

| Location Type | Zoom Level | Style | Use Case |
|---------------|------------|-------|----------|
| **Country** | 4 | world | Country boundaries, continental view |
| **City/Community** | 11 | navigation | Urban areas, city overview |  
| **Address** | 16 | navigation | Street-level, building details |

### Location Type Detection

Location types are determined from the geocoding service's `Addr_type` attribute:

**Country-level:**
- `Country`, `Admin1`, `State`, `Province`

**Address-level:** 
- `StreetAddress`, `PointAddress`, `BuildingName`, `Street`, `Address`

**City-level (default):**
- `Locality`, `Populated Place`, `AdminDivision3`
- Any unrecognized or missing `Addr_type`

### Sample Usage by Location Type

```python
# Country-level requests → zoom 4, world style
country_map = render_static_map_from_location("Germany")
continent_map = render_static_map_from_location("Europe")

# City-level requests → zoom 11, navigation style  
city_map = render_static_map_from_location("Bonn, Germany")
town_map = render_static_map_from_location("Kyoto, Japan")

# Address-level requests → zoom 16, navigation style
address_map = render_static_map_from_location("1600 Pennsylvania Ave NW, Washington, DC")
building_map = render_static_map_from_location("Beethovenallee 22, 53173 Bonn, Germany")
```

## Zoom Level Guidelines

### Zoom Level Selection
- **1-3**: World/continent view
- **4-6**: Country/large region view
- **7-10**: State/province view
- **11-13**: City view
- **14-16**: Neighborhood view (default)
- **17-20**: Street/building view

### Use Case Recommendations
```python
# Different contexts require different zoom levels
zoom_levels = {
    "country": 6,
    "state": 8,
    "city": 10,
    "neighborhood": 15,  # Default
    "street": 18,
    "building": 20
}

# Generate map for specific context
city_map = display_location_on_map("Paris, France", zoom_level=zoom_levels["city"])
street_map = display_location_on_map("123 Main St, Paris", zoom_level=zoom_levels["street"])
```

## Advanced Features

### Multi-Platform Support
```python
# Access all map platforms
display_package = display_location_on_map("Central Park, NYC")
if display_package["success"]:
    urls = display_package["map_urls"]
    
    # Use different platforms for different purposes
    google_for_directions = urls["google_maps"]
    osm_for_open_source = urls["openstreetmap"] 
    arcgis_for_analysis = urls["arcgis"]
```

### Custom Styling Options
Future enhancements may include:
- Custom map themes and colors
- Marker customization
- Layer overlays
- Interactive controls configuration

### Integration with Other Services
Maps can be combined with other location services:
```python
# Display location with elevation data
elevation_display = display_location_with_elevation("Mount Whitney, CA")
# Includes map display with elevation information

# Show route on map
directions = get_directions("San Francisco", "Oakland")
# Route geometry can be used for map visualization
```

## Performance Optimization

### Caching Strategies
```python
# Cache map URLs for frequently accessed locations
map_cache = {}

def get_cached_map_urls(address, zoom_level):
    key = f"{address}|{zoom_level}"
    if key not in map_cache:
        map_cache[key] = generate_map_url(address, zoom_level)
    return map_cache[key]
```

### Loading Optimization
- **Lazy loading**: Maps load only when needed
- **Responsive sizing**: Appropriate dimensions for context
- **Fallback handling**: Graceful degradation when services unavailable

### Best Practices
- Use appropriate zoom levels for context
- Cache generated URLs for performance
- Provide multiple map service options
- Handle network failures gracefully
- Test map embeds in target environments

## Error Handling

### Common Error Scenarios
- **Geocoding failure**: Address cannot be resolved
- **Map service unavailable**: External service issues
- **Invalid zoom level**: Out-of-range zoom values
- **Network connectivity**: Internet connection problems

### Error Response Structure
```json
{
    "success": false,
    "address": "Invalid Address",
    "error": "Geocoding failed for Invalid Address: Address not found",
    "map_urls": null,
    "embed_html": null
}
```

### Fallback Strategies
- Display coordinate-based maps when geocoding fails
- Provide text-based location information
- Offer alternative map services
- Show cached results when available

## Testing

The map visualization service includes comprehensive tests:
```bash
# Run map-specific tests
python src/mcp/test_geocoding.py  # Includes map functionality tests
```

Test coverage includes:
- Map URL generation
- HTML embed creation
- Multiple platform support
- Error handling scenarios
- Responsive design validation
- Performance benchmarks