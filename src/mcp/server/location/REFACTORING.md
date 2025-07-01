# MCP Location Server Implementation Documentation

## Overview

The MCP Location Server provides a robust and modular framework for location-based services. This document explains the current architecture and its components, detailing how they work together to deliver functionality.

## Architecture

### Components

1. **LocationServer Class** (`location_server_class.py`)
   - Encapsulates server registration logic for reusability.
   - Manages the server lifecycle, including creation, startup, and shutdown.
   - Validates configurations and injects dependencies.
   - Provides comprehensive logging and error handling.

2. **Server Configuration** (`server_config.py`)
   - Centralized configuration management for the server.
   - Supports custom server settings and capability validation.
   - Ensures a clear separation between configuration and business logic.

3. **Entry Point** (`server_main.py`)
   - Acts as the main entry point for starting the server.
   - Demonstrates clean dependency wiring and minimal startup code.
   - Simplifies customization for different deployment scenarios.

4. **Location Services** (`location_server.py`)
   - Implements core location-based functionalities, such as geocoding, map rendering, and basemap tile retrieval.
   - Integrates with the `LocationServer` class for server registration.
   - Provides tools for generating static maps, handling bounding boxes, and supporting multiple basemap styles.

## Key Features

- **Modularity**: The architecture separates server setup from business logic, making it easier to maintain and extend.
- **Reusability**: The `LocationServer` class can be reused across different projects and contexts.
- **Testability**: Comprehensive unit tests ensure reliability and allow for mocking dependencies during testing.
- **Extensibility**: The design allows for easy addition of new features, configuration options, and capabilities.
- **Error Handling**: Robust error handling mechanisms ensure stability and provide detailed logs for debugging.

## Usage

- **Starting the Server**: Use `server_main.py` to start the server with the desired configuration.
- **Customizing Configuration**: Modify `server_config.py` to adjust server settings and capabilities.
- **Adding New Features**: Extend `location_server.py` or create new modules to add functionality while leveraging the existing framework.

## Unit Testing

### Running Unit Tests

To run the unit tests for the MCP Location Server, use the following command:

```bash
python -m unittest discover -s src/mcp -p "test_*.py"
```

This command discovers and runs all test files matching the pattern `test_*.py` in the `src/mcp` directory.

### Test Coverage

The unit tests cover the following cases:

1. **Geocoding Functionality**
   - Validates geocoding results for various input addresses.
   - Tests error handling for invalid or empty addresses.

2. **Static Basemap Tile Retrieval**
   - Ensures correct tile URLs are generated for given coordinates and zoom levels.
   - Tests handling of invalid coordinates and zoom levels.

3. **Bounding Box Tile Retrieval**
   - Verifies that the correct tiles are returned for a given bounding box and zoom level.
   - Tests edge cases, such as bounding boxes crossing the International Date Line.

4. **Map Rendering**
   - Validates the rendering of static maps for different styles and zoom levels.
   - Ensures compatibility with various basemap styles and configurations.

5. **Configuration Management**
   - Tests loading and validation of server configurations.
   - Ensures proper error handling for invalid configurations.

6. **Server Lifecycle Management**
   - Verifies the creation, startup, and shutdown of the `LocationServer` class.
   - Tests logging and error handling during the server lifecycle.

These tests ensure the reliability and robustness of the MCP Location Server's implementation.

This document serves as a guide to understanding and working with the MCP Location Server's current implementation.