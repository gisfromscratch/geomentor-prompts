# Places Services

## Overview
The Places service provides point-of-interest discovery and nearby search functionality using the ArcGIS Places API. This service enables finding restaurants, gas stations, hotels, and other businesses or landmarks around specific locations with advanced filtering and categorization.

## Available Tools

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

## Resource Endpoints

### `places://{location}`
Direct access to places information near a location address.

**Example:** `places://Times Square, New York, NY`

**Returns:** Formatted overview of nearby places

### `places://{latitude},{longitude}`
Direct access to places information near specific coordinates.

**Example:** `places://40.7589,-73.9851`

**Returns:** Formatted overview of places near the coordinates

## Supported Categories

The places search supports extensive category filtering:

### Food & Dining
- `restaurant` - Restaurants and food establishments
- `fast_food` - Quick service restaurants
- `cafe` - Coffee shops and cafes
- `bar` - Bars and pubs
- `bakery` - Bakeries and pastry shops

### Transportation
- `gas_station` - Gas stations and fuel services
- `parking` - Parking lots and garages
- `subway_station` - Public transit stations
- `airport` - Airports and aviation facilities

### Accommodation
- `hotel` - Hotels and accommodations
- `lodging` - All types of lodging facilities

### Health & Services
- `hospital` - Hospitals and medical facilities
- `pharmacy` - Pharmacies and drug stores
- `bank` - Banks and financial services
- `atm` - ATM locations

### Shopping & Entertainment
- `shopping_mall` - Shopping centers and malls
- `store` - Retail stores
- `movie_theater` - Cinemas and theaters
- `tourist_attraction` - Tourist attractions and landmarks

### Recreation & Outdoors
- `park` - Parks and recreational areas
- `gym` - Fitness centers and gyms
- `museum` - Museums and cultural sites

### Education & Public
- `school` - Schools and educational institutions
- `library` - Public libraries
- `police` - Police stations
- `fire_station` - Fire departments

## Usage Examples

### Find Restaurants
```python
# Find restaurants near a specific address
places_result = find_places("Times Square, New York, NY", category="restaurant", radius=500, max_results=5)
if places_result["success"]:
    print(f"Found {places_result['results']['total_found']} restaurants")
    
    for place in places_result['results']['places']:
        print(f"- {place['name']}: {place['address']} ({place['distance']}m away)")
        if 'rating' in place:
            print(f"  Rating: {place['rating']}/5")
        if 'price_level' in place:
            print(f"  Price: {place['price_level']}")
```

### Find Any Type of Place
```python
# Find any type of place near coordinates (no category filter)
all_places = find_places_by_coordinates(40.7589, -73.9851, radius=1000, max_results=20)
if all_places["success"]:
    print(all_places['chat_summary'])  # Human-friendly summary
    
    # Group places by category
    by_category = {}
    for place in all_places['results']['places']:
        for cat in place['categories']:
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(place['name'])
    
    for category, places in by_category.items():
        print(f"{category}: {', '.join(places[:3])}")
```

### Interactive Map Display
```python
# Display places on an interactive map
places_result = find_places("Downtown Seattle", category="coffee", radius=800)
if places_result["success"]:
    # Display places on map
    print(places_result['map_visualization']['search_area_html'])  # HTML for embedding
    
    # Show search center map URLs
    urls = places_result['map_visualization']['search_center_urls']
    print(f"View search area: {urls['google_maps']}")
```

### Nearby Services
```python
# Find essential services (gas, ATM, pharmacy)
essential_services = ['gas_station', 'atm', 'pharmacy']
location = "1600 Amphitheatre Parkway, Mountain View, CA"

for service in essential_services:
    result = find_places(location, category=service, radius=2000, max_results=3)
    if result["success"] and result['results']['places']:
        closest = result['results']['places'][0]
        print(f"Nearest {service}: {closest['name']} ({closest['distance']}m)")
```

### Error Handling
```python
# Handle search failures gracefully
result = find_places("Invalid Location XYZ", category="restaurant")
if not result["success"]:
    print(f"Places search failed: {result['error']}")
```

## API Integration

### ArcGIS Places API
This service integrates with the ArcGIS Places API which provides:
- Global point-of-interest database
- Rich place metadata and attributes
- Category-based filtering
- Distance-based search capabilities
- Real-time place information

### Data Sources
Places data is aggregated from multiple sources:
- **Business directories**: Commercial establishment databases
- **Government data**: Public facility registries
- **Crowdsourced content**: Community-contributed information
- **Real-time updates**: Dynamic business information

### Authentication
```python
# Using environment variable (recommended)
export ARCGIS_API_KEY="your_api_key_here"

# Or pass API key directly
places = find_places(location, category="restaurant", api_key="your_api_key")
```

## Response Format Details

### Place Information
Each place includes comprehensive details:
- `name`: Business or place name
- `place_id`: Unique identifier for the place
- `categories`: Array of applicable categories
- `address`: Full formatted address
- `coordinates`: Precise latitude/longitude
- `distance`: Distance from search center in meters
- `phone`: Contact phone number (when available)
- `website`: Official website URL (when available)
- `rating`: User rating (1-5 scale, when available)
- `price_level`: Price indicator ($, $$, $$$, $$$$)

### Search Query Details
- `location`: Original search location input
- `geocoded_address`: Standardized address from geocoding
- `coordinates`: Search center coordinates
- `category_filter`: Applied category filter
- `radius_meters`: Search radius in meters
- `max_results`: Maximum results requested

### Map Visualization
- `search_center_urls`: Map URLs for the search location
- `search_area_html`: Embeddable HTML showing places on map

## Performance Optimization

### Search Parameters
- **Radius**: Use appropriate radius for your use case
  - 500m: Walking distance
  - 1000m: Short drive/bike ride
  - 5000m: Wider area search
- **Max results**: Limit results to improve performance
- **Category filtering**: Use specific categories for focused searches

### Caching Strategies
```python
# Cache places results for frequently searched areas
places_cache = {}

def get_cached_places(location, category, radius):
    key = f"{location}|{category}|{radius}"
    if key not in places_cache:
        places_cache[key] = find_places(location, category, radius)
    return places_cache[key]
```

### Best Practices
- Use coordinate-based search when precise location is known
- Filter by category to reduce irrelevant results
- Consider user context when setting search radius
- Handle empty results gracefully
- Respect API rate limits for high-volume applications

## Error Handling

### Common Error Scenarios
- **Location not found**: Invalid or ambiguous search location
- **No places found**: No matching places in search area
- **Category not supported**: Invalid category filter
- **Network issues**: Connectivity or API availability problems

### Error Response Structure
```json
{
    "success": false,
    "error": "Failed to geocode location 'Invalid Location': Address not found",
    "search_query": {
        "location": "Invalid Location",
        "category_filter": "restaurant",
        "radius_meters": 1000
    }
}
```

## Testing

The places service includes comprehensive tests:
```bash
# Run places-specific tests
python src/mcp/test_places.py
```

Test coverage includes:
- Valid place searches
- Category filtering
- Invalid location handling
- Empty result scenarios
- Map visualization generation
- Error response validation
- Performance benchmarks