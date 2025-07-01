#!/usr/bin/env python3
"""
Entry point for the MCP Location Server

This script demonstrates the minimal entry point approach using the
refactored LocationServer class. It handles dependency wiring and
server startup with clean separation of concerns.
"""

import sys
import logging
from location_server_class import LocationServer
from server_config import LocationServerConfig, MCPServerConfig


def main():
    """
    Main entry point for the MCP Location Server
    
    This function demonstrates how to use the LocationServer class
    for different deployment scenarios with custom configuration.
    """
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        # Option 1: Use default configuration
        server = LocationServer()
        
        # Option 2: Use custom configuration (example)
        # custom_config = LocationServerConfig.get_server_config(
        #     name="Custom Location Server",
        #     port=8001,
        #     transport="sse"
        # )
        # server = LocationServer(custom_config)
        
        # Start the server
        server.start()
        
    except KeyboardInterrupt:
        print("\\nReceived interrupt signal. Shutting down server...")
        server.stop()
        sys.exit(0)
    except Exception as e:
        print(f"Failed to start server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()