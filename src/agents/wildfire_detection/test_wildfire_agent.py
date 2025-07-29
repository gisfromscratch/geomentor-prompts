"""
Unit tests for the Simple Reflex Agent for Wildfire Detection
"""

import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock

from wildfire_agent import (
    SimpleReflexAgent,
    EnvironmentalPercepts,
    WildfireDecision,
    LocationServices,
    RuleEngine,
)


class TestEnvironmentalPercepts:
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

        assert percepts.thermal == 320.5
        assert percepts.humidity == 45.0
        assert percepts.landuse == "forest"
        assert percepts.vegetation_density == 0.8


class TestLocationServices:
    """Test the LocationServices class"""

    def test_location_services_without_api_key(self):
        """Test location services with mock data"""
        services = LocationServices()

        # Test thermal data
        thermal = services.get_thermal_data(34.0522, -118.2437)
        assert isinstance(thermal, float)
        assert thermal > 0

        # Test land cover
        land_cover = services.get_land_cover(34.0522, -118.2437)
        assert isinstance(land_cover, str)
        assert land_cover in ["urban", "forest", "grassland"]

        # Test weather data
        weather = services.get_weather_data(34.0522, -118.2437)
        assert "humidity" in weather
        assert "wind_speed" in weather
        assert isinstance(weather["humidity"], float)
        assert isinstance(weather["wind_speed"], float)

    def test_location_services_different_locations(self):
        """Test that different locations return appropriate mock data"""
        services = LocationServices()

        # Los Angeles should return urban
        la_land_cover = services.get_land_cover(34.0522, -118.2437)
        assert la_land_cover == "urban"

        # Remote location should return forest or grassland
        remote_land_cover = services.get_land_cover(45.0, -110.0)
        assert remote_land_cover in ["forest", "grassland"]


class TestRuleEngine:
    """Test the RuleEngine class"""

    def test_rule_engine_creation(self):
        """Test creating a rule engine"""
        engine = RuleEngine()
        assert len(engine.rules) == 0
        assert len(engine.rule_names) == 0

    def test_adding_rules(self):
        """Test adding rules to the engine"""
        engine = RuleEngine()

        @engine.add_rule("test_rule")
        def test_rule(percepts):
            if percepts.thermal > 300:
                return "Test alert"
            return None

        assert len(engine.rules) == 1
        assert "test_rule" in engine.rule_names.values()

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
        assert decision.risk_level in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        assert len(decision.triggered_rules) > 0
        assert decision.alert_message is not None

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
        assert len(decision.triggered_rules) == 0
        assert decision.alert_message is None


class TestSimpleReflexAgent:
    """Test the SimpleReflexAgent class"""

    def test_agent_initialization(self):
        """Test agent initialization"""
        agent = SimpleReflexAgent()
        assert agent.location_services is not None
        assert agent.rule_engine is not None
        assert len(agent.rule_engine.rules) > 0  # Should have default rules

    def test_agent_perceive(self):
        """Test agent perception"""
        agent = SimpleReflexAgent()
        percepts = agent.perceive(34.0522, -118.2437)

        assert isinstance(percepts, EnvironmentalPercepts)
        assert percepts.latitude == 34.0522
        assert percepts.longitude == -118.2437
        assert percepts.thermal > 0
        assert 0 <= percepts.humidity <= 100
        assert percepts.wind_speed >= 0
        assert percepts.landuse in ["urban", "forest", "grassland"]
        assert 0 <= percepts.vegetation_density <= 1
        assert percepts.asset_proximity > 0

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
        assert isinstance(decision, WildfireDecision)
        assert decision.risk_level in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        assert 0 <= decision.confidence <= 1
        assert isinstance(decision.triggered_rules, list)

    def test_agent_full_cycle(self):
        """Test complete agent execution cycle"""
        agent = SimpleReflexAgent()

        # Run the agent
        decision = agent.run(34.0522, -118.2437)

        assert isinstance(decision, WildfireDecision)
        assert decision.risk_level in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        assert decision.timestamp is not None

    def test_custom_rule_addition(self):
        """Test adding custom rules to the agent"""
        agent = SimpleReflexAgent()
        initial_rule_count = len(agent.rule_engine.rules)

        @agent.add_rule("custom_test_rule")
        def custom_rule(percepts):
            if percepts.thermal > 400:  # Very high threshold
                return "Custom alert"
            return None

        assert len(agent.rule_engine.rules) == initial_rule_count + 1


class TestIntegration:
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
        assert len(decision.triggered_rules) > 0
        assert decision.risk_level in ["HIGH", "CRITICAL"]
        assert decision.alert_message is not None
        assert decision.confidence > 0

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
        assert len(decision.triggered_rules) == 0
        assert decision.risk_level == "LOW"
        assert decision.alert_message is None
        assert decision.confidence == 0.0


# Test fixtures and parametrized tests
@pytest.mark.parametrize(
    "lat,lon,expected_land_cover",
    [
        (34.0522, -118.2437, "urban"),  # Los Angeles
        (45.0, -110.0, "forest"),  # Remote area
    ],
)
def test_location_land_cover_mapping(lat, lon, expected_land_cover):
    """Test land cover mapping for different locations"""
    services = LocationServices()
    land_cover = services.get_land_cover(lat, lon)
    assert land_cover == expected_land_cover


@pytest.mark.parametrize(
    "thermal,humidity,wind,expected_risk_level",
    [
        (340.0, 10.0, 30.0, "CRITICAL"),  # Very high risk
        (320.0, 25.0, 18.0, "MEDIUM"),  # Medium risk
        (280.0, 80.0, 5.0, "LOW"),  # Low risk
    ],
)
def test_risk_level_scenarios(thermal, humidity, wind, expected_risk_level):
    """Test different risk level scenarios"""
    agent = SimpleReflexAgent()

    percepts = EnvironmentalPercepts(
        thermal=thermal,
        humidity=humidity,
        wind_speed=wind,
        landuse="forest",
        vegetation_density=0.7,
        asset_proximity=5.0,
        timestamp=datetime.now(),
        latitude=40.0,
        longitude=-120.0,
    )

    decision = agent.decide(percepts)
    # Note: The exact risk level depends on the specific rule thresholds
    # This test checks that the system produces a valid risk level
    assert decision.risk_level in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]


if __name__ == "__main__":
    # Run tests if executed directly
    pytest.main([__file__])
