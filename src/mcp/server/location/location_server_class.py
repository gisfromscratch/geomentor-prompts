"""
LocationServer class for MCP Location Services

This module provides a reusable LocationServer class that encapsulates
server registration, configuration, and lifecycle management for the
MCP Location Server.
"""

import logging
from typing import Optional
from mcp.server.fastmcp import FastMCP

from server_config import LocationServerConfig, MCPServerConfig
from location_config import ArcGISApiKeyManager


class LocationServer:
    """
    Reusable MCP Location Server class
    
    This class encapsulates the server registration logic, configuration management,
    and lifecycle operations for the MCP Location Server, making it easy to reuse
    across different deployments and test scenarios.
    """
    
    def __init__(self, config: Optional[MCPServerConfig] = None):
        """
        Initialize the LocationServer
        
        Args:
            config: Optional server configuration. If None, uses default config.
        """
        self.config = config or LocationServerConfig.get_server_config()
        self.mcp_server = None
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the server"""
        logger = logging.getLogger(f"LocationServer-{self.config.name}")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
        
    def create_server(self) -> FastMCP:
        """
        Create and configure the FastMCP server instance
        
        Returns:
            FastMCP: Configured MCP server instance
        """
        if self.mcp_server is not None:
            raise RuntimeError("Server already created. Use get_server() to access existing instance.")
            
        self.logger.info(f"Creating MCP server: {self.config.name}")
        
        # Create FastMCP server with configuration
        server_params = self.config.to_dict()
        self.mcp_server = FastMCP(**server_params)
        
        self.logger.info(f"MCP server created successfully on port {self.config.port}")
        return self.mcp_server
        
    def get_server(self) -> FastMCP:
        """
        Get the MCP server instance, creating it if it doesn't exist
        
        Returns:
            FastMCP: The MCP server instance
        """
        if self.mcp_server is None:
            return self.create_server()
        return self.mcp_server
        
    def register_tools_and_resources(self):
        """
        Register all tools and resources with the MCP server
        
        This method will be called to set up all the location service endpoints.
        The actual tool registration is handled by importing and decorating
        functions from the location services modules.
        """
        if self.mcp_server is None:
            raise RuntimeError("Server not created. Call create_server() first.")
            
        self.logger.info("Registering location service tools and resources...")
        
        # Tools and resources are registered via decorators in location_server.py
        # This method serves as a hook for additional registration logic if needed
        capabilities = LocationServerConfig.get_supported_capabilities()
        self.logger.info(f"Server supports capabilities: {', '.join(capabilities)}")
        
        # Initialize place categories cache during startup
        self.logger.info("Initializing place categories cache...")
        try:
            from location_server import get_cached_categories
            categories_result = get_cached_categories()
            if categories_result["success"]:
                self.logger.info(f"Loaded {categories_result['total_count']} place categories")
            else:
                self.logger.warning(f"Failed to load place categories: {categories_result['error']}")
        except Exception as e:
            self.logger.warning(f"Error initializing place categories cache: {e}")
        
    def validate_configuration(self) -> bool:
        """
        Validate server configuration and dependencies
        
        Returns:
            bool: True if configuration is valid, False otherwise
        """
        try:
            # Check API key availability
            api_key = ArcGISApiKeyManager.get_api_key()
            if not api_key:
                self.logger.warning("No ArcGIS API key found in environment variables")
                self.logger.warning("Some location services may not function properly")
            else:
                self.logger.info("ArcGIS API key found and configured")
                
            # Validate port availability
            if not (1 <= self.config.port <= 65535):
                self.logger.error(f"Invalid port number: {self.config.port}")
                return False
                
            # Validate transport
            if self.config.transport not in ["stdio", "sse"]:
                self.logger.error(f"Unsupported transport: {self.config.transport}")
                return False
                
            self.logger.info("Server configuration validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Configuration validation failed: {e}")
            return False
            
    def start(self):
        """
        Start the MCP server
        
        This method validates configuration, creates the server,
        registers tools/resources, and starts the server.
        """
        try:
            self.logger.info("Starting Location MCP Server...")
            
            # Validate configuration
            if not self.validate_configuration():
                raise RuntimeError("Server configuration validation failed")
                
            # Create server if not already created
            server = self.get_server()
            
            # Register tools and resources
            self.register_tools_and_resources()
            
            # Start the server with configured transport
            self.logger.info(f"Starting server with transport: {self.config.transport}")
            server.run(transport=self.config.transport)
            
        except Exception as e:
            self.logger.error(f"Failed to start server: {e}")
            raise
            
    def stop(self):
        """
        Stop the MCP server
        
        This method provides a clean shutdown mechanism.
        """
        if self.mcp_server:
            self.logger.info("Stopping Location MCP Server...")
            # FastMCP doesn't have a direct stop method, but we can clean up
            self.mcp_server = None
            self.logger.info("Server stopped")
            
    def get_server_info(self) -> dict:
        """
        Get information about the server configuration and status
        
        Returns:
            dict: Server information including config and status
        """
        return {
            "name": self.config.name,
            "description": self.config.description,
            "version": self.config.version,
            "port": self.config.port,
            "transport": self.config.transport,
            "server_created": self.mcp_server is not None,
            "capabilities": LocationServerConfig.get_supported_capabilities(),
            "api_key_configured": ArcGISApiKeyManager.get_api_key() is not None
        }