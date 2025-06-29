"""
Core functionality tests focusing on the refactored components

This test module focuses on testing the core components that were refactored
without importing the full location_server.py that has Image type issues.
"""

import unittest
import unittest.mock
import os
import sys
from unittest.mock import Mock, patch

# Add the location server directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server_config import LocationServerConfig, MCPServerConfig
from location_config import ArcGISApiKeyManager
from location_server_class import LocationServer


class TestRefactoredComponents(unittest.TestCase):
    """Test the refactored components without importing problematic modules"""
    
    def test_server_config_module_independence(self):
        """Test that server config module works independently"""
        config = LocationServerConfig.get_server_config(
            name="Independent Test",
            port=9876
        )
        
        self.assertEqual(config.name, "Independent Test")
        self.assertEqual(config.port, 9876)
        
    def test_location_server_class_independence(self):
        """Test that LocationServer class works independently"""
        config = MCPServerConfig(name="Test", port=8888)
        server = LocationServer(config)
        
        # Test basic functionality without creating actual server
        self.assertEqual(server.config.name, "Test")
        self.assertTrue(server.validate_configuration())
        
        info = server.get_server_info()
        self.assertEqual(info["name"], "Test")
        self.assertFalse(info["server_created"])
        
    @patch('location_server_class.FastMCP')
    def test_server_creation_isolated(self, mock_fastmcp):
        """Test server creation in isolation"""
        mock_server = Mock()
        mock_fastmcp.return_value = mock_server
        
        config = MCPServerConfig(name="Isolated Test")
        server = LocationServer(config)
        
        created_server = server.create_server()
        
        # Verify the server was created correctly
        self.assertEqual(created_server, mock_server)
        mock_fastmcp.assert_called_once_with(**config.to_dict())
        
    def test_api_key_manager_functionality(self):
        """Test ArcGIS API key manager functionality"""
        # Test with explicit key
        explicit_key = "test_explicit_key_12345"
        result = ArcGISApiKeyManager.get_api_key(explicit_key)
        self.assertEqual(result, explicit_key)
        
        # Test parameter addition
        params = {"existing": "value"}
        ArcGISApiKeyManager.add_key_to_params(params, explicit_key)
        
        self.assertIn("token", params)
        self.assertEqual(params["token"], explicit_key)
        self.assertEqual(params["existing"], "value")  # Existing param preserved
        
    def test_logging_configuration(self):
        """Test logging is properly configured in LocationServer"""
        server = LocationServer()
        
        # Should have a logger configured
        self.assertIsNotNone(server.logger)
        self.assertTrue(len(server.logger.handlers) > 0)
        
        # Logger name should include server name
        self.assertIn("LocationServer", server.logger.name)
        
    def test_configuration_validation_logic(self):
        """Test configuration validation logic"""
        # Test valid configurations
        valid_configs = [
            MCPServerConfig(port=8000, transport="stdio"),
            MCPServerConfig(port=65535, transport="sse"),
            MCPServerConfig(port=1, transport="stdio"),
        ]
        
        for config in valid_configs:
            server = LocationServer(config)
            self.assertTrue(server.validate_configuration(), 
                          f"Config should be valid: {config}")
                          
        # Test invalid configurations
        invalid_configs = [
            MCPServerConfig(port=0),      # Invalid port
            MCPServerConfig(port=70000),  # Invalid port
            MCPServerConfig(transport="invalid"),  # Invalid transport
        ]
        
        for config in invalid_configs:
            server = LocationServer(config)
            self.assertFalse(server.validate_configuration(), 
                           f"Config should be invalid: {config}")
                           
    def test_capabilities_reporting(self):
        """Test that capabilities are properly reported"""
        capabilities = LocationServerConfig.get_supported_capabilities()
        
        # Should be a non-empty list
        self.assertIsInstance(capabilities, list)
        self.assertGreater(len(capabilities), 0)
        
        # Should contain expected core capabilities
        expected_core = ["geocoding", "elevation_services", "places_search"]
        for capability in expected_core:
            self.assertIn(capability, capabilities)
            
    @patch('location_server_class.FastMCP')
    def test_complete_lifecycle_flow(self, mock_fastmcp):
        """Test complete server lifecycle without problematic imports"""
        mock_server = Mock()
        mock_fastmcp.return_value = mock_server
        
        # Create server
        config = MCPServerConfig(name="Lifecycle Test", port=7777)
        server = LocationServer(config)
        
        # Test initial state
        self.assertIsNone(server.mcp_server)
        
        # Create and register
        server.create_server()
        server.register_tools_and_resources()
        
        # Verify state
        self.assertIsNotNone(server.mcp_server)
        info = server.get_server_info()
        self.assertTrue(info["server_created"])
        
        # Stop server
        server.stop()
        self.assertIsNone(server.mcp_server)
        
    def test_multiple_server_instances(self):
        """Test that multiple server instances can coexist"""
        config1 = MCPServerConfig(name="Server1", port=8001)
        config2 = MCPServerConfig(name="Server2", port=8002)
        
        server1 = LocationServer(config1)
        server2 = LocationServer(config2)
        
        # Should be independent
        self.assertNotEqual(server1.config.name, server2.config.name)
        self.assertNotEqual(server1.config.port, server2.config.port)
        
        # Should have different loggers
        self.assertNotEqual(server1.logger.name, server2.logger.name)


class TestConfigurationEdgeCases(unittest.TestCase):
    """Test edge cases in configuration management"""
    
    def test_config_to_dict_completeness(self):
        """Test that config.to_dict() includes all necessary parameters"""
        config = MCPServerConfig(
            name="Complete Test",
            description="Complete Description", 
            version="1.2.3",
            port=9999
        )
        
        config_dict = config.to_dict()
        
        # Should include all necessary keys for FastMCP
        required_keys = {"name", "description", "version", "port"}
        self.assertEqual(set(config_dict.keys()), required_keys)
        
        # Values should match
        self.assertEqual(config_dict["name"], "Complete Test")
        self.assertEqual(config_dict["description"], "Complete Description")
        self.assertEqual(config_dict["version"], "1.2.3")
        self.assertEqual(config_dict["port"], 9999)
        
    def test_override_behavior(self):
        """Test parameter override behavior in LocationServerConfig"""
        # Test partial overrides
        config = LocationServerConfig.get_server_config(
            name="Partial Override",
            port=5555
        )
        
        # Overridden values
        self.assertEqual(config.name, "Partial Override")
        self.assertEqual(config.port, 5555)
        
        # Non-overridden values should be defaults
        self.assertEqual(config.description, LocationServerConfig.DEFAULT_CONFIG.description)
        self.assertEqual(config.version, LocationServerConfig.DEFAULT_CONFIG.version)
        self.assertEqual(config.transport, LocationServerConfig.DEFAULT_CONFIG.transport)
        
    def test_none_override_handling(self):
        """Test that None values in overrides use defaults"""
        config = LocationServerConfig.get_server_config(
            name=None,  # Should use default
            port=4444   # Should use override
        )
        
        self.assertEqual(config.name, LocationServerConfig.DEFAULT_CONFIG.name)
        self.assertEqual(config.port, 4444)


if __name__ == '__main__':
    unittest.main(verbosity=2)