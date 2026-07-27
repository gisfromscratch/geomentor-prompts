"""
Unit tests for the Simple Reflex Agent for Wildfire Detection
"""

import unittest
from datetime import datetime
import os
import sys
from unittest.mock import patch, MagicMock

# Add the wildfire_agent directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
print(sys.path)

from wildfire_agent import (
    SimpleReflexAgent,
    EnvironmentalPercepts,
    WildfireDecision,
    LocationServices,
    RuleEngine,
)


class TestEnvironmentalPercepts(unittest.TestCase):
    """Test the EnvironmentalPercepts dataclass"""

    def test_percepts_creation(self):
        """Test creating environmental percepts"""
        percepts = EnvironmentalPercepts(
            thermal=320.5,
            humidity=45.0,
            wind_speed=12.0,
            landuse="forest",
            vegetation_density=0.8,
            asset_proximity=5.0,
            timestamp=datetime.now(),
            latitude=34.0522,
            longitude=-118.2437,
        )

        self.assertEqual(percepts.thermal, 320.5)
        self.assertEqual(percepts.humidity, 45.0)
        self.assertEqual(percepts.landuse, "forest")
        self.assertEqual(percepts.vegetation_density, 0.8)


class TestLocationServices(unittest.TestCase):
    """Test the LocationServices class"""

    def test_location_services_without_api_key(self):
        """Test location services with mock data"""
        services = LocationServices()

        # Test thermal data
        thermal = services.get_thermal_data(34.0522, -118.2437)
        self.assertIsInstance(thermal, float)
        self.assertGreater(thermal, 0)

        # Test land cover
        land_cover = services.get_land_cover(34.0522, -118.2437)
        self.assertIsInstance(land_cover, str)
        self.assertIn(land_cover, ["urban", "forest", "grassland"])

        # Test weather data
        weather = services.get_weather_data(34.0522, -118.2437)
        self.assertIn("humidity", weather)
        self.assertIn("wind_speed", weather)
        self.assertIsInstance(weather["humidity"], float)
        self.assertIsInstance(weather["wind_speed"], float)

    def test_location_services_different_locations(self):
        """Test that different locations return appropriate mock data"""
        services = LocationServices()

        # Los Angeles should return urban
        la_land_cover = services.get_land_cover(34.0522, -118.2437)
        self.assertEqual(la_land_cover, "urban")

        # Remote location should return forest or grassland
        remote_land_cover = services.get_land_cover(45.0, -110.0)
        self.assertIn(remote_land_cover, ["forest", "grassland"])


class TestRuleEngine(unittest.TestCase):
    """Test the RuleEngine class"""

    def test_rule_engine_creation(self):
        """Test creating a rule engine"""
        engine = RuleEngine()
        self.assertEqual(len(engine.rules), 0)
        self.assertEqual(len(engine.rule_names), 0)

    def test_adding_rules(self):
        """Test adding rules to the engine"""
        engine = RuleEngine()

        @engine.add_rule("test_rule")
        def test_rule(percepts):
            if percepts.thermal > 300:
                return "Test alert"
            return None

        self.assertEqual(len(engine.rules), 1)
        self.assertIn("test_rule", engine.rule_names.values())

    def test_rule_evaluation(self):
        """Test rule evaluation"""
        engine = RuleEngine()

        @engine.add_rule("high_temp_rule")
        def high_temp_rule(percepts):
            if percepts.thermal > 330:
                return "HIGH temperature alert"
            return None

        # Test with high temperature
        high_temp_percepts = EnvironmentalPercepts(
            thermal=340.0,
            humidity=30.0,
            wind_speed=10.0,
            landuse="forest",
            vegetation_density=0.5,
            asset_proximity=10.0,
            timestamp=datetime.now(),
            latitude=40.0,
            longitude=-120.0,
        )

        decision = engine.evaluate(high_temp_percepts)
        self.assertIn(decision.risk_level, ["LOW", "MEDIUM", "HIGH", "CRITICAL"])
        self.assertGreater(len(decision.triggered_rules), 0)
        self.assertIsNotNone(decision.alert_message)

        # Test with normal temperature
        normal_temp_percepts = EnvironmentalPercepts(
            thermal=290.0,
            humidity=60.0,
            wind_speed=5.0,
            landuse="urban",
            vegetation_density=0.2,
            asset_proximity=2.0,
            timestamp=datetime.now(),
            latitude=40.0,
            longitude=-120.0,
        )

        decision = engine.evaluate(normal_temp_percepts)
        self.assertEqual(len(decision.triggered_rules), 0)
        self.assertIsNone(decision.alert_message)


class TestSimpleReflexAgent(unittest.TestCase):
    """Test the SimpleReflexAgent class"""

    def test_agent_initialization(self):
        """Test agent initialization"""
        agent = SimpleReflexAgent()
        self.assertIsNotNone(agent.location_services)
        self.assertIsNotNone(agent.rule_engine)
        self.assertGreater(len(agent.rule_engine.rules), 0)  # Should have default rules

    def test_agent_perceive(self):
        """Test agent perception"""
        agent = SimpleReflexAgent()
        percepts = agent.perceive(34.0522, -118.2437)

        self.assertIsInstance(percepts, EnvironmentalPercepts)
        self.assertEqual(percepts.latitude, 34.0522)
        self.assertEqual(percepts.longitude, -118.2437)
        self.assertGreater(percepts.thermal, 0)
        self.assertGreaterEqual(percepts.humidity, 0)
        self.assertLessEqual(percepts.humidity, 100)
        self.assertGreaterEqual(percepts.wind_speed, 0)
        self.assertIn(percepts.landuse, ["urban", "forest", "grassland"])
        self.assertGreaterEqual(percepts.vegetation_density, 0)
        self.assertLessEqual(percepts.vegetation_density, 1)
        self.assertGreater(percepts.asset_proximity, 0)

    def test_agent_decide(self):
        """Test agent decision making"""
        agent = SimpleReflexAgent()

        # Create test percepts
        percepts = EnvironmentalPercepts(
            thermal=335.0,  # High temperature
            humidity=15.0,  # Low humidity
            wind_speed=25.0,  # High wind
            landuse="forest",
            vegetation_density=0.9,  # Dense vegetation
            asset_proximity=3.0,  # Close to assets
            timestamp=datetime.now(),
            latitude=34.0522,
            longitude=-118.2437,
        )

        decision = agent.decide(percepts)
        self.assertIsInstance(decision, WildfireDecision)
        self.assertIn(decision.risk_level, ["LOW", "MEDIUM", "HIGH", "CRITICAL"])
        self.assertGreaterEqual(decision.confidence, 0)
        self.assertLessEqual(decision.confidence, 1)
        self.assertIsInstance(decision.triggered_rules, list)

    def test_agent_full_cycle(self):
        """Test complete agent execution cycle"""
        agent = SimpleReflexAgent()

        # Run the agent
        decision = agent.run(34.0522, -118.2437)

        self.assertIsInstance(decision, WildfireDecision)
        self.assertIn(decision.risk_level, ["LOW", "MEDIUM", "HIGH", "CRITICAL"])
        self.assertIsNotNone(decision.timestamp)

    def test_custom_rule_addition(self):
        """Test adding custom rules to the agent"""
        agent = SimpleReflexAgent()
        initial_rule_count = len(agent.rule_engine.rules)

        @agent.add_rule("custom_test_rule")
        def custom_rule(percepts):
            if percepts.thermal > 400:  # Very high threshold
                return "Custom alert"
            return None

        self.assertEqual(len(agent.rule_engine.rules), initial_rule_count + 1)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system"""

    def test_high_risk_scenario(self):
        """Test a high-risk wildfire scenario"""
        agent = SimpleReflexAgent()

        # Create high-risk percepts
        high_risk_percepts = EnvironmentalPercepts(
            thermal=340.0,  # Very high temperature
            humidity=10.0,  # Very low humidity
            wind_speed=30.0,  # Very high wind
            landuse="forest",
            vegetation_density=0.95,  # Very dense vegetation
            asset_proximity=1.0,  # Very close to assets
            timestamp=datetime.now(),
            latitude=34.0522,
            longitude=-118.2437,
        )

        decision = agent.decide(high_risk_percepts)

        # Should trigger multiple rules and have high risk
        self.assertGreater(len(decision.triggered_rules), 0)
        self.assertIn(decision.risk_level, ["HIGH", "CRITICAL"])
        self.assertIsNotNone(decision.alert_message)
        self.assertGreater(decision.confidence, 0)

    def test_low_risk_scenario(self):
        """Test a low-risk scenario"""
        agent = SimpleReflexAgent()

        # Create low-risk percepts
        low_risk_percepts = EnvironmentalPercepts(
            thermal=280.0,  # Low temperature
            humidity=80.0,  # High humidity
            wind_speed=5.0,  # Low wind
            landuse="urban",
            vegetation_density=0.1,  # Low vegetation
            asset_proximity=0.5,  # Close to assets but urban
            timestamp=datetime.now(),
            latitude=37.7749,
            longitude=-122.4194,
        )

        decision = agent.decide(low_risk_percepts)

        # Should not trigger rules and have low risk
        self.assertEqual(len(decision.triggered_rules), 0)
        self.assertEqual(decision.risk_level, "LOW")
        self.assertIsNone(decision.alert_message)
        self.assertEqual(decision.confidence, 0.0)


class TestLocationLandCoverMapping(unittest.TestCase):
    """Test land cover mapping for different locations"""

    def test_los_angeles_land_cover(self):
        """Test Los Angeles land cover mapping"""
        services = LocationServices()
        land_cover = services.get_land_cover(34.0522, -118.2437)
        self.assertEqual(land_cover, "urban")

    def test_remote_area_land_cover(self):
        """Test remote area land cover mapping"""
        services = LocationServices()
        land_cover = services.get_land_cover(45.0, -110.0)
        self.assertEqual(land_cover, "forest")


class TestValidationGuardrails(unittest.TestCase):
    """Test validation guardrails for filtering noise and invalid data"""

    def setUp(self):
        """Set up test agent"""
        self.agent = SimpleReflexAgent()

    def test_valid_percepts(self):
        """Test that valid percepts pass validation"""
        valid_percepts = EnvironmentalPercepts(
            thermal=320.5,
            humidity=45.0,
            wind_speed=12.0,
            landuse="forest",
            vegetation_density=0.8,
            asset_proximity=5.0,
            timestamp=datetime.now(),
            latitude=34.0522,
            longitude=-118.2437,
        )
        self.assertTrue(self.agent.validate(valid_percepts))

    def test_none_thermal_fails(self):
        """Test that None thermal data fails validation"""
        invalid_percepts = EnvironmentalPercepts(
            thermal=None,
            humidity=45.0,
            wind_speed=12.0,
            landuse="forest",
            vegetation_density=0.8,
            asset_proximity=5.0,
            timestamp=datetime.now(),
            latitude=34.0522,
            longitude=-118.2437,
        )
        self.assertFalse(self.agent.validate(invalid_percepts))

    def test_none_humidity_fails(self):
        """Test that None humidity data fails validation"""
        invalid_percepts = EnvironmentalPercepts(
            thermal=320.5,
            humidity=None,
            wind_speed=12.0,
            landuse="forest",
            vegetation_density=0.8,
            asset_proximity=5.0,
            timestamp=datetime.now(),
            latitude=34.0522,
            longitude=-118.2437,
        )
        self.assertFalse(self.agent.validate(invalid_percepts))

    def test_negative_thermal_fails(self):
        """Test that negative thermal data fails validation"""
        invalid_percepts = EnvironmentalPercepts(
            thermal=-10.0,
            humidity=45.0,
            wind_speed=12.0,
            landuse="forest",
            vegetation_density=0.8,
            asset_proximity=5.0,
            timestamp=datetime.now(),
            latitude=34.0522,
            longitude=-118.2437,
        )
        self.assertFalse(self.agent.validate(invalid_percepts))

    def test_invalid_humidity_range_fails(self):
        """Test that humidity outside 0-100 range fails validation"""
        # Test negative humidity
        invalid_percepts = EnvironmentalPercepts(
            thermal=320.5,
            humidity=-5.0,
            wind_speed=12.0,
            landuse="forest",
            vegetation_density=0.8,
            asset_proximity=5.0,
            timestamp=datetime.now(),
            latitude=34.0522,
            longitude=-118.2437,
        )
        self.assertFalse(self.agent.validate(invalid_percepts))

        # Test humidity over 100
        invalid_percepts.humidity = 150.0
        self.assertFalse(self.agent.validate(invalid_percepts))

    def test_unrealistic_thermal_range_fails(self):
        """Test that unrealistic thermal values fail validation"""
        # Test extremely low temperature (below realistic Earth range)
        invalid_percepts = EnvironmentalPercepts(
            thermal=100.0,  # Too cold for surface temperature
            humidity=45.0,
            wind_speed=12.0,
            landuse="forest",
            vegetation_density=0.8,
            asset_proximity=5.0,
            timestamp=datetime.now(),
            latitude=34.0522,
            longitude=-118.2437,
        )
        self.assertFalse(self.agent.validate(invalid_percepts))

        # Test extremely high temperature
        invalid_percepts.thermal = 500.0  # Too hot for surface temperature
        self.assertFalse(self.agent.validate(invalid_percepts))

    def test_invalid_wind_speed_fails(self):
        """Test that invalid wind speed values fail validation"""
        # Test negative wind speed
        invalid_percepts = EnvironmentalPercepts(
            thermal=320.5,
            humidity=45.0,
            wind_speed=-5.0,
            landuse="forest",
            vegetation_density=0.8,
            asset_proximity=5.0,
            timestamp=datetime.now(),
            latitude=34.0522,
            longitude=-118.2437,
        )
        self.assertFalse(self.agent.validate(invalid_percepts))

        # Test unrealistically high wind speed
        invalid_percepts.wind_speed = 500.0  # Unrealistic wind speed
        self.assertFalse(self.agent.validate(invalid_percepts))

    def test_invalid_vegetation_density_fails(self):
        """Test that vegetation density outside 0-1 range fails validation"""
        # Test negative vegetation density
        invalid_percepts = EnvironmentalPercepts(
            thermal=320.5,
            humidity=45.0,
            wind_speed=12.0,
            landuse="forest",
            vegetation_density=-0.1,
            asset_proximity=5.0,
            timestamp=datetime.now(),
            latitude=34.0522,
            longitude=-118.2437,
        )
        self.assertFalse(self.agent.validate(invalid_percepts))

        # Test vegetation density over 1.0
        invalid_percepts.vegetation_density = 1.5
        self.assertFalse(self.agent.validate(invalid_percepts))

    def test_invalid_asset_proximity_fails(self):
        """Test that negative asset proximity fails validation"""
        invalid_percepts = EnvironmentalPercepts(
            thermal=320.5,
            humidity=45.0,
            wind_speed=12.0,
            landuse="forest",
            vegetation_density=0.8,
            asset_proximity=-1.0,
            timestamp=datetime.now(),
            latitude=34.0522,
            longitude=-118.2437,
        )
        self.assertFalse(self.agent.validate(invalid_percepts))

    def test_invalid_coordinates_fail(self):
        """Test that invalid geographic coordinates fail validation"""
        # Test invalid latitude (> 90)
        invalid_percepts = EnvironmentalPercepts(
            thermal=320.5,
            humidity=45.0,
            wind_speed=12.0,
            landuse="forest",
            vegetation_density=0.8,
            asset_proximity=5.0,
            timestamp=datetime.now(),
            latitude=95.0,  # Invalid latitude
            longitude=-118.2437,
        )
        self.assertFalse(self.agent.validate(invalid_percepts))

        # Test invalid longitude (> 180)
        invalid_percepts.latitude = 34.0522
        invalid_percepts.longitude = 185.0  # Invalid longitude
        self.assertFalse(self.agent.validate(invalid_percepts))

    def test_invalid_landuse_fails(self):
        """Test that invalid landuse values fail validation"""
        invalid_percepts = EnvironmentalPercepts(
            thermal=320.5,
            humidity=45.0,
            wind_speed=12.0,
            landuse="invalid_landuse",  # Not in allowed categories
            vegetation_density=0.8,
            asset_proximity=5.0,
            timestamp=datetime.now(),
            latitude=34.0522,
            longitude=-118.2437,
        )
        self.assertFalse(self.agent.validate(invalid_percepts))

    def test_none_values_for_critical_fields(self):
        """Test that None values for critical fields fail validation"""
        # Test None wind_speed
        invalid_percepts = EnvironmentalPercepts(
            thermal=320.5,
            humidity=45.0,
            wind_speed=None,
            landuse="forest",
            vegetation_density=0.8,
            asset_proximity=5.0,
            timestamp=datetime.now(),
            latitude=34.0522,
            longitude=-118.2437,
        )
        self.assertFalse(self.agent.validate(invalid_percepts))

        # Test None vegetation_density
        invalid_percepts.wind_speed = 12.0
        invalid_percepts.vegetation_density = None
        self.assertFalse(self.agent.validate(invalid_percepts))


class TestRiskLevelScenarios(unittest.TestCase):
    """Test different risk level scenarios"""

    def test_very_high_risk_scenario(self):
        """Test very high risk scenario"""
        agent = SimpleReflexAgent()

        percepts = EnvironmentalPercepts(
            thermal=340.0,
            humidity=10.0,
            wind_speed=30.0,
            landuse="forest",
            vegetation_density=0.7,
            asset_proximity=5.0,
            timestamp=datetime.now(),
            latitude=40.0,
            longitude=-120.0,
        )

        decision = agent.decide(percepts)
        self.assertIn(decision.risk_level, ["LOW", "MEDIUM", "HIGH", "CRITICAL"])

    def test_medium_risk_scenario(self):
        """Test medium risk scenario"""
        agent = SimpleReflexAgent()

        percepts = EnvironmentalPercepts(
            thermal=320.0,
            humidity=25.0,
            wind_speed=18.0,
            landuse="forest",
            vegetation_density=0.7,
            asset_proximity=5.0,
            timestamp=datetime.now(),
            latitude=40.0,
            longitude=-120.0,
        )

        decision = agent.decide(percepts)
        self.assertIn(decision.risk_level, ["LOW", "MEDIUM", "HIGH", "CRITICAL"])

    def test_low_risk_scenario(self):
        """Test low risk scenario"""
        agent = SimpleReflexAgent()

        percepts = EnvironmentalPercepts(
            thermal=280.0,
            humidity=80.0,
            wind_speed=5.0,
            landuse="forest",
            vegetation_density=0.7,
            asset_proximity=5.0,
            timestamp=datetime.now(),
            latitude=40.0,
            longitude=-120.0,
        )

        decision = agent.decide(percepts)
        self.assertIn(decision.risk_level, ["LOW", "MEDIUM", "HIGH", "CRITICAL"])


if __name__ == "__main__":
    # Run tests if executed directly
    unittest.main()
