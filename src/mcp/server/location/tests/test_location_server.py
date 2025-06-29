"""
Unit tests for the MCP Location Server

This test module provides comprehensive coverage of the refactored
LocationServer class, configuration management, and core functionality
using Python's built-in unittest framework.
"""

import unittest
import unittest.mock
import os
import sys
from unittest.mock import Mock, patch, MagicMock

# Add the location server directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server_config import LocationServerConfig, MCPServerConfig
from location_config import ArcGISApiKeyManager
from location_server_class import LocationServer


class TestMCPServerConfig(unittest.TestCase):
    """Test cases for MCPServerConfig"""
    
    def test_default_configuration(self):
        """Test default configuration values"""
        config = MCPServerConfig()
        
        self.assertEqual(config.name, "Location MCP Demo")
        self.assertEqual(config.description, "A MCP demo server for location-based services")
        self.assertEqual(config.version, "0.1.0")
        self.assertEqual(config.port, 8000)
        self.assertEqual(config.transport, "stdio")
        
    def test_custom_configuration(self):
        """Test custom configuration values"""
        config = MCPServerConfig(
            name="Test Server",
            description="Test Description",
            version="1.0.0",
            port=9000,
            transport="sse"
        )
        
        self.assertEqual(config.name, "Test Server")
        self.assertEqual(config.description, "Test Description")
        self.assertEqual(config.version, "1.0.0")
        self.assertEqual(config.port, 9000)
        self.assertEqual(config.transport, "sse")
        
    def test_to_dict_conversion(self):
        """Test configuration to dictionary conversion"""
        config = MCPServerConfig(name="Test", port=9000)
        config_dict = config.to_dict()
        
        expected_keys = {"name", "description", "version", "port"}
        self.assertEqual(set(config_dict.keys()), expected_keys)
        self.assertEqual(config_dict["name"], "Test")
        self.assertEqual(config_dict["port"], 9000)


class TestLocationServerConfig(unittest.TestCase):
    """Test cases for LocationServerConfig"""
    
    def test_get_default_server_config(self):
        """Test getting default server configuration"""
        config = LocationServerConfig.get_server_config()
        
        self.assertIsInstance(config, MCPServerConfig)
        self.assertEqual(config.name, LocationServerConfig.DEFAULT_CONFIG.name)
        
    def test_get_server_config_with_overrides(self):
        """Test server configuration with parameter overrides"""
        config = LocationServerConfig.get_server_config(
            name="Override Name",
            port=7000,
            transport="sse"
        )
        
        self.assertEqual(config.name, "Override Name")
        self.assertEqual(config.port, 7000)
        self.assertEqual(config.transport, "sse")
        # Non-overridden values should remain default
        self.assertEqual(config.version, LocationServerConfig.DEFAULT_CONFIG.version)
        
    def test_get_supported_capabilities(self):
        """Test supported capabilities list"""
        capabilities = LocationServerConfig.get_supported_capabilities()
        
        self.assertIsInstance(capabilities, list)
        self.assertIn("geocoding", capabilities)
        self.assertIn("elevation_services", capabilities)
        self.assertIn("places_search", capabilities)
        self.assertTrue(len(capabilities) > 0)


class TestArcGISApiKeyManager(unittest.TestCase):
    """Test cases for ArcGISApiKeyManager"""
    
    def test_explicit_api_key(self):
        """Test using explicit API key"""
        test_key = "test_explicit_key"
        result = ArcGISApiKeyManager.get_api_key(test_key)
        self.assertEqual(result, test_key)
        
    @patch.dict(os.environ, {"ARCGIS_API_KEY": "test_env_key"})
    def test_environment_api_key(self):
        """Test retrieving API key from environment"""
        result = ArcGISApiKeyManager.get_api_key()
        self.assertEqual(result, "test_env_key")
        
    @patch.dict(os.environ, {}, clear=True)
    def test_no_api_key_found(self):
        """Test when no API key is available"""
        result = ArcGISApiKeyManager.get_api_key()
        self.assertIsNone(result)
        
    def test_add_key_to_params(self):
        """Test adding API key to parameters"""
        params = {"test": "value"}
        test_key = "test_token_key"
        
        ArcGISApiKeyManager.add_key_to_params(params, test_key)
        
        self.assertIn("token", params)
        self.assertEqual(params["token"], test_key)
        
    @patch.dict(os.environ, {}, clear=True)
    def test_add_key_to_params_no_key(self):
        """Test adding API key to parameters when no key available"""
        params = {"test": "value"}
        
        ArcGISApiKeyManager.add_key_to_params(params)
        
        # Should not add token key if no API key available
        self.assertNotIn("token", params)


class TestLocationServer(unittest.TestCase):
    """Test cases for LocationServer class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_config = MCPServerConfig(
            name="Test Location Server",
            port=9999,
            transport="stdio"
        )
        
    def test_server_initialization(self):
        """Test LocationServer initialization"""
        server = LocationServer(self.test_config)
        
        self.assertEqual(server.config, self.test_config)
        self.assertIsNone(server.mcp_server)
        self.assertIsNotNone(server.logger)
        
    def test_server_initialization_default_config(self):
        """Test LocationServer with default configuration"""
        server = LocationServer()
        
        self.assertIsInstance(server.config, MCPServerConfig)
        self.assertEqual(server.config.name, LocationServerConfig.DEFAULT_CONFIG.name)
        
    @patch('location_server_class.FastMCP')
    def test_create_server(self, mock_fastmcp):
        """Test server creation"""
        mock_server_instance = Mock()
        mock_fastmcp.return_value = mock_server_instance
        
        server = LocationServer(self.test_config)
        result = server.create_server()
        
        # Verify FastMCP was called with correct parameters
        mock_fastmcp.assert_called_once_with(**self.test_config.to_dict())
        self.assertEqual(result, mock_server_instance)
        self.assertEqual(server.mcp_server, mock_server_instance)
        
    @patch('location_server_class.FastMCP')
    def test_create_server_already_exists(self, mock_fastmcp):
        """Test creating server when one already exists"""
        server = LocationServer(self.test_config)
        server.mcp_server = Mock()  # Simulate existing server
        
        with self.assertRaises(RuntimeError) as context:
            server.create_server()
            
        self.assertIn("Server already created", str(context.exception))
        
    @patch('location_server_class.FastMCP')
    def test_get_server(self, mock_fastmcp):
        """Test getting server instance"""
        mock_server_instance = Mock()
        mock_fastmcp.return_value = mock_server_instance
        
        server = LocationServer(self.test_config)
        result = server.get_server()
        
        # Should create server if it doesn't exist
        self.assertEqual(result, mock_server_instance)
        
        # Second call should return same instance
        result2 = server.get_server()
        self.assertEqual(result2, mock_server_instance)
        mock_fastmcp.assert_called_once()  # Should only create once
        
    def test_register_tools_and_resources_no_server(self):
        """Test registering tools when no server exists"""
        server = LocationServer(self.test_config)
        
        with self.assertRaises(RuntimeError) as context:
            server.register_tools_and_resources()
            
        self.assertIn("Server not created", str(context.exception))
        
    @patch('location_server_class.FastMCP')
    def test_register_tools_and_resources(self, mock_fastmcp):
        """Test registering tools and resources"""
        mock_server_instance = Mock()
        mock_fastmcp.return_value = mock_server_instance
        
        server = LocationServer(self.test_config)
        server.create_server()
        
        # Should not raise exception
        server.register_tools_and_resources()
        
    @patch.dict(os.environ, {"ARCGIS_API_KEY": "test_key"})
    def test_validate_configuration_success(self):
        """Test successful configuration validation"""
        server = LocationServer(self.test_config)
        result = server.validate_configuration()
        
        self.assertTrue(result)
        
    def test_validate_configuration_invalid_port(self):
        """Test configuration validation with invalid port"""
        invalid_config = MCPServerConfig(port=70000)  # Invalid port
        server = LocationServer(invalid_config)
        
        result = server.validate_configuration()
        self.assertFalse(result)
        
    def test_validate_configuration_invalid_transport(self):
        """Test configuration validation with invalid transport"""
        invalid_config = MCPServerConfig(transport="invalid")
        server = LocationServer(invalid_config)
        
        result = server.validate_configuration()
        self.assertFalse(result)
        
    @patch('location_server_class.FastMCP')
    def test_start_server_success(self, mock_fastmcp):
        """Test successful server start"""
        mock_server_instance = Mock()
        mock_fastmcp.return_value = mock_server_instance
        
        server = LocationServer(self.test_config)
        
        with patch.object(server, 'validate_configuration', return_value=True):
            server.start()
            
        # Verify server.run was called with correct transport
        mock_server_instance.run.assert_called_once_with(transport=self.test_config.transport)
        
    @patch('location_server_class.FastMCP')
    def test_start_server_validation_failure(self, mock_fastmcp):
        """Test server start with validation failure"""
        server = LocationServer(self.test_config)
        
        with patch.object(server, 'validate_configuration', return_value=False):
            with self.assertRaises(RuntimeError) as context:
                server.start()
                
        self.assertIn("validation failed", str(context.exception))
        
    def test_stop_server(self):
        """Test server stop"""
        server = LocationServer(self.test_config)
        server.mcp_server = Mock()
        
        server.stop()
        
        self.assertIsNone(server.mcp_server)
        
    @patch.dict(os.environ, {"ARCGIS_API_KEY": "test_key"})
    def test_get_server_info(self):
        """Test getting server information"""
        server = LocationServer(self.test_config)
        info = server.get_server_info()
        
        self.assertIsInstance(info, dict)
        self.assertEqual(info["name"], self.test_config.name)
        self.assertEqual(info["port"], self.test_config.port)
        self.assertEqual(info["transport"], self.test_config.transport)
        self.assertFalse(info["server_created"])
        self.assertTrue(info["api_key_configured"])
        self.assertIn("capabilities", info)


if __name__ == '__main__':
    unittest.main(verbosity=2)