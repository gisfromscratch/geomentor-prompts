# MCP Location Server Refactoring Documentation

## Overview

The MCP Location Server has been refactored to improve modularity, reusability, and testability while maintaining all existing functionality. This document describes the new architecture and how to use it.

## Refactored Architecture

### Components

1. **LocationServer Class** (`location_server_class.py`)
   - Encapsulates server registration logic for reusability
   - Provides clean lifecycle management (create, start, stop)
   - Handles configuration validation and dependency injection
   - Includes comprehensive logging and error handling

2. **Server Configuration** (`server_config.py`)
   - Centralized configuration management
   - Support for custom server settings
   - Capability reporting and validation
   - Separation of concerns between config and business logic

3. **Minimal Entry Point** (`server_main.py`)
   - Demonstrates clean dependency wiring
   - Minimal code focused on startup and shutdown
   - Easy to customize for different deployment scenarios

4. **Original Location Services** (`location_server.py`)
   - All existing functionality preserved
   - Now uses the LocationServer class for registration
   - Maintains backward compatibility

### Benefits of Refactoring

- **Modularity**: Server setup is separated from business logic
- **Reusability**: LocationServer class can be used in multiple contexts
- **Testability**: Comprehensive unittest coverage with mocking
- **Maintainability**: Clear separation of concerns and better error handling
- **Extensibility**: Easy to add new configuration options and capabilities

## Usage Examples

### Basic Usage (Default Configuration)

```python
from location_server_class import LocationServer

# Create and start server with defaults
server = LocationServer()
server.start()
```

### Custom Configuration

```python
from location_server_class import LocationServer
from server_config import LocationServerConfig, MCPServerConfig

# Create custom configuration
config = LocationServerConfig.get_server_config(
    name="Custom Location Server",
    description="Production location services",
    port=8001,
    transport="sse"
)

# Use custom configuration
server = LocationServer(config)
server.start()
```

### Programmatic Server Management

```python
from location_server_class import LocationServer

# Create server instance
server = LocationServer()

# Validate configuration before starting
if server.validate_configuration():
    # Create server and register tools
    mcp_server = server.create_server()
    server.register_tools_and_resources()
    
    # Get server information
    info = server.get_server_info()
    print(f"Server: {info['name']} on port {info['port']}")
    
    # Start server
    server.start()
else:
    print("Configuration validation failed")
```

### Multiple Server Instances

```python
from location_server_class import LocationServer
from server_config import MCPServerConfig

# Create multiple servers for different purposes
dev_config = MCPServerConfig(name="Dev Server", port=8000)
prod_config = MCPServerConfig(name="Prod Server", port=8001)

dev_server = LocationServer(dev_config)
prod_server = LocationServer(prod_config)

# Each server is independent
dev_server.start()  # Runs on port 8000
# prod_server.start()  # Would run on port 8001
```

## Configuration Options

### MCPServerConfig Parameters

- `name`: Server name (default: "Location MCP Demo")
- `description`: Server description (default: "A MCP demo server for location-based services")
- `version`: Server version (default: "0.1.0")
- `port`: Server port (default: 8000)
- `transport`: Transport protocol - "stdio" or "sse" (default: "stdio")

### Supported Capabilities

The server supports the following capabilities:

- `geocoding` - Address to coordinate conversion
- `reverse_geocoding` - Coordinate to address conversion
- `elevation_services` - Terrain elevation data
- `routing_directions` - Turn-by-turn directions
- `places_search` - Nearby places discovery
- `map_visualization` - Interactive map generation
- `static_basemap_tiles` - Static map tile rendering

## Testing

### Running All Tests

```bash
# Run all tests
python -m unittest discover tests/ -v

# Run specific test modules
python -m unittest tests.test_location_server -v
python -m unittest tests.test_core_functionality -v
python -m unittest tests.test_integration -v
```

### Test Coverage

The test suite covers:

- **Server Registration**: LocationServer class creation and management
- **Configuration Management**: All configuration scenarios and validation
- **Edge Cases**: Invalid configurations, missing dependencies, error handling
- **Integration**: Complete server lifecycle and component interaction
- **Mocking**: External dependencies (FastMCP, API services) are mocked

### Test Structure

```
tests/
├── __init__.py                    # Test package initialization
├── test_location_server.py        # Core LocationServer class tests
├── test_integration.py            # Integration and lifecycle tests
└── test_core_functionality.py     # Focused component tests
```

## Error Handling

The refactored server includes robust error handling:

### Configuration Validation
- Port range validation (1-65535)
- Transport protocol validation ("stdio" or "sse")
- API key availability checking (warns if missing)

### Server Lifecycle
- Prevents duplicate server creation
- Validates configuration before startup
- Graceful shutdown handling
- Comprehensive logging at all stages

### API Dependencies
- Graceful handling of missing ArcGIS API keys
- Clear warnings about reduced functionality
- Fallback behaviors for network issues

## Migration Guide

### For Existing Users

The refactoring is backward compatible:

```python
# Old way (still works)
python location_server.py

# New way (recommended)
python server_main.py
```

### For Developers

To extend the server:

1. **Add New Configuration Options**:
   ```python
   # Add to MCPServerConfig in server_config.py
   @dataclass
   class MCPServerConfig:
       # ... existing fields ...
       new_option: str = "default_value"
   ```

2. **Add New Capabilities**:
   ```python
   # Add to LocationServerConfig.get_supported_capabilities()
   def get_supported_capabilities(cls) -> List[str]:
       return [
           # ... existing capabilities ...
           "new_capability"
       ]
   ```

3. **Customize Server Behavior**:
   ```python
   class CustomLocationServer(LocationServer):
       def register_tools_and_resources(self):
           super().register_tools_and_resources()
           # Add custom registration logic
   ```

## Known Issues and Limitations

### Image Type Compatibility
Some functions in the original `location_server.py` return `Union[Image, Dict]` where `Image` is from `mcp.server.fastmcp.Image`. This can cause pydantic schema generation errors in certain MCP framework versions. This is an existing issue in the original codebase, not introduced by the refactoring.

**Workaround**: The refactored components work independently and can be tested separately from the full location_server.py module.

### API Key Configuration
The server requires an ArcGIS API key for full functionality. Set the `ARCGIS_API_KEY` environment variable:

```bash
export ARCGIS_API_KEY="your_api_key_here"
python server_main.py
```

## Performance Considerations

- Configuration validation is performed once at startup
- Server instances are lightweight and can coexist
- Logging is configurable and doesn't impact performance
- All external dependencies are loaded on-demand

## Future Enhancements

Planned improvements:
- Dynamic configuration reloading without restart
- Health check endpoints
- Metrics and monitoring integration
- Docker containerization support
- Advanced error recovery mechanisms

## Support

For issues or questions about the refactored server:
1. Check the test suite for usage examples
2. Review the configuration options in `server_config.py`
3. Examine the LocationServer class documentation in `location_server_class.py`
4. Run tests to verify your environment setup