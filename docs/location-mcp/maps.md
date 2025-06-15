# Map Visualization Services

## Overview
The Map Visualization service provides interactive map generation, URL creation, and embed HTML for displaying locations, routes, and places in chat interfaces and web applications. This service integrates with multiple mapping platforms to provide comprehensive map display capabilities.

## Available Tools

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