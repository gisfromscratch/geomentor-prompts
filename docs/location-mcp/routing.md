# Routing Services

## Overview
The Routing service provides turn-by-turn directions and travel optimization between locations using the ArcGIS World Route Service. This service supports multiple travel modes and provides comprehensive route information including travel time, distance, and detailed navigation instructions.

## Available Tools

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

## Travel Modes

### Driving
- **Mode**: `"driving"`
- **Use case**: Standard passenger vehicle routing
- **Features**: Avoids restricted roads, considers traffic patterns
- **Speed limits**: Based on road classifications

### Walking
- **Mode**: `"walking"`
- **Use case**: Pedestrian navigation
- **Features**: Uses sidewalks and pedestrian paths
- **Accessibility**: Considers walkable routes only

### Trucking
- **Mode**: `"trucking"`
- **Use case**: Commercial vehicle routing
- **Features**: Avoids truck restrictions, considers vehicle limitations
- **Considerations**: Height, weight, and hazmat restrictions

## Usage Examples

### Basic Driving Directions
```python
# Get driving directions between addresses
directions = get_directions("San Francisco, CA", "Oakland, CA", travel_mode="driving")
if directions["success"]:
    summary = directions["route_summary"]
    print(f"Travel time: {summary['total_time_formatted']}")
    print(f"Distance: {summary['total_distance_miles']} miles")
    
    # Display formatted directions
    print(directions["formatted_directions"])
```

### Walking Directions
```python
# Get walking directions using coordinates
walking_dirs = get_directions("37.7749,-122.4194", "37.8049,-122.4194", travel_mode="walking")
if walking_dirs["success"]:
    print(f"Walking time: {walking_dirs['route_summary']['total_time_formatted']}")
    
    # Show first 5 turn-by-turn directions
    for i, step in enumerate(walking_dirs["directions"][:5], 1):
        print(f"{i}. {step['instruction']}")
```

### Commercial Vehicle Routing
```python
# Get trucking directions with restrictions
truck_route = get_directions(
    "Los Angeles Distribution Center", 
    "San Diego Warehouse", 
    travel_mode="trucking"
)
if truck_route["success"]:
    print("Truck-optimized route:")
    print(f"Distance: {truck_route['route_summary']['total_distance_miles']} miles")
    print(f"Estimated time: {truck_route['route_summary']['total_time_formatted']}")
```

### Coordinate-Based Routing
```python
# Use precise coordinates for routing
precise_route = get_directions(
    "34.0522,-118.2437",  # Los Angeles coordinates
    "32.7157,-117.1611",  # San Diego coordinates
    travel_mode="driving"
)
```

### Error Handling
```python
# Handle routing failures gracefully
result = get_directions("Invalid Location", "Another Invalid Location")
if not result["success"]:
    print(f"Routing failed: {result['error']}")
    print(f"Origin: {result['origin']}")
    print(f"Destination: {result['destination']}")
```

## API Integration

### ArcGIS World Route Service
This service integrates with the ArcGIS World Route Service which provides:
- Global routing coverage
- Real-time traffic considerations
- Multiple transportation modes
- Turn-by-turn navigation instructions
- Route optimization algorithms

### Route Calculation Features
- **Shortest path**: Optimized for distance
- **Fastest route**: Optimized for travel time
- **Avoid restrictions**: Respects road limitations
- **Traffic awareness**: Considers current conditions (where available)

### Authentication
```python
# Using environment variable (recommended)
export ARCGIS_API_KEY="your_api_key_here"

# Or pass API key directly
directions = get_directions(origin, destination, api_key="your_api_key")
```

## Response Format Details

### Route Summary
- `total_time_minutes`: Travel time in decimal minutes
- `total_distance_miles`: Total distance in miles
- `total_time_formatted`: Human-readable time format

### Turn-by-Turn Directions
Each direction step includes:
- `instruction`: Human-readable navigation instruction
- `distance`: Segment distance in miles
- `time`: Segment travel time in minutes
- `maneuver_type`: Technical maneuver classification

### Formatted Output
The `formatted_directions` field provides chat-ready output:
```
🗺️ **Driving Directions**
📍 From: San Francisco, CA
📍 To: Oakland, CA
⏱️ Total Time: 25 minutes
📏 Total Distance: 12.3 miles

1. Head north on Main St (0.5 mi, 2 min)
2. Turn right onto Highway 101 (8.2 mi, 15 min)
...
```

### Error Response Structure
```json
{
    "success": false,
    "origin": "input origin",
    "destination": "input destination",
    "travel_mode": "driving",
    "error": "Error description"
}
```

## Route Optimization

### Travel Mode Selection
Choose the appropriate travel mode based on your use case:
- **Driving**: General passenger vehicle use
- **Walking**: Pedestrian navigation and exercise
- **Trucking**: Commercial delivery and freight

### Performance Considerations
- **Geocoding**: Addresses are automatically geocoded for routing
- **Caching**: Cache routes for frequently traveled paths
- **Batch processing**: Group multiple route requests efficiently

### Route Quality Factors
- **Accuracy**: Depends on road network data quality
- **Real-time data**: Traffic conditions when available
- **Regional coverage**: Varies by geographic location
- **Update frequency**: Road network changes and updates

## Advanced Features

### Route Geometry
The `route_geometry` field contains the geographic path of the route for mapping applications:
```python
if directions["success"]:
    geometry = directions["route_geometry"]
    # Use geometry for drawing route on maps
```

### Custom Routing Parameters
Future enhancements may include:
- Avoid toll roads
- Avoid highways
- Shortest vs fastest preferences
- Vehicle-specific restrictions

## Best Practices

### Input Validation
```python
def validate_routing_input(origin, destination, travel_mode):
    if not origin or not destination:
        return False, "Origin and destination required"
    
    valid_modes = ["driving", "walking", "trucking"]
    if travel_mode not in valid_modes:
        return False, f"Travel mode must be one of: {valid_modes}"
    
    return True, "Valid input"

# Use validation before routing
is_valid, message = validate_routing_input(origin, dest, mode)
if is_valid:
    directions = get_directions(origin, dest, mode)
```

### Error Recovery
- Check `success` field before using route data
- Provide fallback options for failed routes
- Handle network timeouts appropriately
- Log errors for debugging and monitoring

### Performance Optimization
- Cache frequent routes to reduce API calls
- Use coordinate inputs when precise locations are known
- Batch process multiple routes when possible
- Consider rate limits for high-volume applications

## Testing

The routing service includes comprehensive tests:
```bash
# Run routing-specific tests
python src/mcp/test_geocoding.py  # Includes routing tests
```

Test coverage includes:
- Valid route calculation
- Invalid address handling
- Different travel modes
- Error response validation
- Direction formatting
- Performance benchmarks