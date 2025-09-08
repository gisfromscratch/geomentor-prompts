"""
Tests for ArcGIS Online search core functionality (without MCP tool dependencies)
"""
import unittest
from unittest.mock import patch, Mock
import sys
import os

# Add parent directory to sys.path to import the modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import only the core function to avoid MCP tool dependency issues
import importlib.util
spec = importlib.util.spec_from_file_location(
    "location_server_funcs", 
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "location_server.py")
)

# Mock the dependencies that would cause issues
with patch('mcp.server.fastmcp.FastMCP'):
    with patch('location_server_class.LocationServer'):
        location_server_funcs = importlib.util.module_from_spec(spec)
        sys.modules["location_server_funcs"] = location_server_funcs
        spec.loader.exec_module(location_server_funcs)


class TestArcGISOnlineSearchCore(unittest.TestCase):
    """Test core ArcGIS Online search functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_arcgis_response = {
            "results": [
                {
                    "id": "test-webmap-id-1",
                    "title": "Forest Cover Analysis Map",
                    "owner": "test_user",
                    "type": "Web Map",
                    "description": "A comprehensive analysis of forest cover",
                    "snippet": "Forest analysis for conservation planning",
                    "tags": ["forest", "conservation", "analysis"],
                    "thumbnail": "thumbnail.png",
                    "access": "public",
                    "numViews": 1500,
                    "avgRating": 4.5,
                    "numRatings": 10,
                    "created": 1640995200000,
                    "modified": 1672531200000,
                    "size": 2048
                },
                {
                    "id": "test-service-id-1",
                    "title": "Forest Monitoring Service",
                    "owner": "forestry_dept",
                    "type": "Feature Service",
                    "description": "Real-time forest monitoring data",
                    "snippet": "Live data from forest sensors",
                    "tags": ["forest", "monitoring", "sensors"],
                    "thumbnail": "service_thumb.png",
                    "access": "public",
                    "numViews": 800,
                    "avgRating": 4.2,
                    "numRatings": 5,
                    "created": 1640995200000,
                    "modified": 1672531200000,
                    "size": 5120,
                    "url": "https://services.arcgis.com/test/arcgis/rest/services/ForestMonitoring/MapServer"
                }
            ],
            "total": 2,
            "start": 1,
            "num": 50
        }
    
    @patch('requests.get')
    def test_search_arcgis_online_success(self, mock_get):
        """Test successful ArcGIS Online search"""
        # Mock successful response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = self.sample_arcgis_response
        mock_get.return_value = mock_response
        
        result = location_server_funcs.search_arcgis_online(
            query="forest",
            item_types=["Web Map", "Feature Service"],
            num=50
        )
        
        # Verify success
        self.assertTrue(result["success"])
        
        # Verify search query structure
        self.assertIn("search_query", result)
        self.assertEqual(result["search_query"]["original_query"], "forest")
        self.assertEqual(result["search_query"]["item_types"], ["Web Map", "Feature Service"])
        
        # Verify results structure
        self.assertIn("results", result)
        self.assertEqual(result["results"]["total_results"], 2)
        self.assertEqual(result["results"]["returned_results"], 2)
        self.assertEqual(len(result["results"]["items"]), 2)
        
        # Verify item metadata
        items = result["results"]["items"]
        
        # Check web map item
        webmap = items[0]
        self.assertEqual(webmap["id"], "test-webmap-id-1")
        self.assertEqual(webmap["title"], "Forest Cover Analysis Map")
        self.assertEqual(webmap["type"], "Web Map")
        self.assertEqual(webmap["num_views"], 1500)
        self.assertEqual(webmap["avg_rating"], 4.5)
        self.assertIn("portal_item_url", webmap)
        self.assertEqual(webmap["portal_item_url"], 
                        "https://www.arcgis.com/home/item.html?id=test-webmap-id-1")
        
        # Check feature service item
        service = items[1]
        self.assertEqual(service["id"], "test-service-id-1")
        self.assertEqual(service["title"], "Forest Monitoring Service")
        self.assertEqual(service["type"], "Feature Service")
        self.assertIn("service_url", service)
        self.assertIn("feature_server_url", service)
        self.assertTrue(service["feature_server_url"].endswith("/FeatureServer"))
    
    @patch('requests.get')
    def test_search_arcgis_online_empty_results(self, mock_get):
        """Test ArcGIS Online search with no results"""
        # Mock empty response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "results": [],
            "total": 0,
            "start": 1,
            "num": 50
        }
        mock_get.return_value = mock_response
        
        result = location_server_funcs.search_arcgis_online(query="nonexistent")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["results"]["total_results"], 0)
        self.assertEqual(len(result["results"]["items"]), 0)
        self.assertIn("message", result)
        self.assertEqual(result["message"], "No results found for the specified criteria")
    
    @patch('requests.get')
    def test_search_arcgis_online_request_error(self, mock_get):
        """Test ArcGIS Online search with request error"""
        # Mock request exception
        mock_get.side_effect = Exception("Network error")
        
        result = location_server_funcs.search_arcgis_online(query="test")
        
        self.assertFalse(result["success"])
        self.assertIn("error", result)
        self.assertIn("ArcGIS Online search error", result["error"])
        self.assertEqual(result["results"]["total_results"], 0)
    
    def test_search_arcgis_online_parameter_validation(self):
        """Test parameter validation and query building"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"results": [], "total": 0}
            mock_get.return_value = mock_response
            
            # Test parameter clamping
            result = location_server_funcs.search_arcgis_online(
                query="test",
                start=0,  # Should be clamped to 1
                num=200,  # Should be clamped to 100
                sort_order="invalid"  # Should default to "desc"
            )
            
            # Check that function was called with correct parameters
            mock_get.assert_called_once()
            call_args = mock_get.call_args
            params = call_args[1]["params"]
            
            self.assertEqual(params["start"], 1)
            self.assertEqual(params["num"], 100)
            self.assertEqual(params["sortOrder"], "desc")
    
    def test_query_building_logic(self):
        """Test query string building logic"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"results": [], "total": 0}
            mock_get.return_value = mock_response
            
            # Test with query and item types
            location_server_funcs.search_arcgis_online(
                query="forest conservation",
                item_types=["Web Map", "Feature Layer"]
            )
            
            call_args = mock_get.call_args
            params = call_args[1]["params"]
            
            # Verify query contains search terms and type filters
            query = params["q"]
            self.assertIn("forest conservation", query)
            self.assertIn('type:"Web Map"', query)
            self.assertIn('type:"Feature Layer"', query)
            self.assertIn("AND", query)
    
    def test_feature_server_url_conversion(self):
        """Test that MapServer URLs are converted to FeatureServer for feature services"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {
                "results": [
                    {
                        "id": "test-id",
                        "title": "Test Service",
                        "type": "Feature Service",
                        "url": "https://services.arcgis.com/test/MapServer/0"
                    }
                ],
                "total": 1
            }
            mock_get.return_value = mock_response
            
            result = location_server_funcs.search_arcgis_online(query="test")
            
            item = result["results"]["items"][0]
            self.assertIn("feature_server_url", item)
            self.assertTrue(item["feature_server_url"].endswith("/FeatureServer"))
            self.assertNotIn("MapServer", item["feature_server_url"])


if __name__ == "__main__":
    unittest.main()