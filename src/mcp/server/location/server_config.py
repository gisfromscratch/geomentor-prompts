"""
Configuration management for the MCP Location Server

This module handles server configuration including MCP server settings,
transport options, and service capabilities.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class MCPServerConfig:
    """Configuration settings for the MCP Location Server"""
    
    name: str = "Location MCP Demo"
    description: str = "A MCP demo server for location-based services"
    version: str = "0.1.0"
    port: int = 8000
    transport: str = "stdio"  # "stdio" or "sse"
    
    def to_dict(self) -> Dict:
        """Convert configuration to dictionary for FastMCP initialization"""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "port": self.port
        }


class LocationServerConfig:
    """Centralized configuration management for the Location Server"""
    
    DEFAULT_CONFIG = MCPServerConfig()
    
    @classmethod
    def get_server_config(cls, 
                         name: Optional[str] = None,
                         description: Optional[str] = None,
                         version: Optional[str] = None,
                         port: Optional[int] = None,
                         transport: Optional[str] = None) -> MCPServerConfig:
        """
        Get server configuration with optional overrides
        
        Args:
            name: Server name override
            description: Server description override  
            version: Server version override
            port: Server port override
            transport: Server transport override
            
        Returns:
            MCPServerConfig: Complete server configuration
        """
        config = MCPServerConfig(
            name=name or cls.DEFAULT_CONFIG.name,
            description=description or cls.DEFAULT_CONFIG.description,
            version=version or cls.DEFAULT_CONFIG.version,
            port=port or cls.DEFAULT_CONFIG.port,
            transport=transport or cls.DEFAULT_CONFIG.transport
        )
        return config
    
    @classmethod
    def get_supported_capabilities(cls) -> List[str]:
        """Get list of supported MCP capabilities"""
        return [
            "geocoding",
            "reverse_geocoding", 
            "elevation_services",
            "routing_directions",
            "places_search",
            "map_visualization",
            "static_basemap_tiles"
        ]