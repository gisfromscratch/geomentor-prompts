"""
Simple Reflex Agent for Wildfire Detection

This module implements a condition-action rule based agent that detects
wildfire risk based on environmental percepts.
"""

import logging
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Callable
from dotenv import load_dotenv
from location import LocationServices

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@dataclass
class EnvironmentalPercepts:
    """Environmental data percepts for wildfire risk assessment"""

    thermal: float  # Temperature in Kelvin
    humidity: float  # Humidity percentage
    wind_speed: float  # Wind speed in km/h
    landuse: str  # Land use classification
    vegetation_density: float  # Vegetation density index (0-1)
    asset_proximity: float  # Distance to nearest asset in km
    timestamp: datetime
    latitude: float
    longitude: float


@dataclass
class WildfireDecision:
    """Decision output from the rule engine"""

    risk_level: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    alert_message: Optional[str]
    confidence: float  # Confidence score (0-1)
    triggered_rules: List[str]  # Names of rules that triggered
    timestamp: datetime


class RuleEngine:
    """Custom rule engine for wildfire detection using condition-action rules"""

    def __init__(self):
        self.rules: List[Callable[[EnvironmentalPercepts], Optional[str]]] = []
        self.rule_names: Dict[Callable, str] = {}

    def add_rule(self, name: str = None):
        """Decorator to add a rule to the engine"""

        def decorator(func: Callable[[EnvironmentalPercepts], Optional[str]]):
            self.rules.append(func)
            self.rule_names[func] = name or func.__name__
            return func

        return decorator

    def evaluate(self, percepts: EnvironmentalPercepts) -> WildfireDecision:
        """Evaluate all rules against the percepts"""
        triggered_rules = []
        alerts = []
        max_risk_level = "LOW"

        # Risk level priority: LOW < MEDIUM < HIGH < CRITICAL
        risk_priority = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}

        for rule in self.rules:
            try:
                result = rule(percepts)
                if result:
                    rule_name = self.rule_names[rule]
                    triggered_rules.append(rule_name)
                    alerts.append(result)

                    # Extract risk level from result
                    if "CRITICAL" in result.upper():
                        max_risk_level = "CRITICAL"
                    elif "HIGH" in result.upper() and risk_priority[max_risk_level] < 2:
                        max_risk_level = "HIGH"
                    elif (
                        "MEDIUM" in result.upper() and risk_priority[max_risk_level] < 1
                    ):
                        max_risk_level = "MEDIUM"
            except Exception as e:
                logger.error(f"Error evaluating rule {self.rule_names[rule]}: {e}")

        # Calculate confidence based on number of triggered rules
        confidence = min(len(triggered_rules) * 0.3, 1.0) if triggered_rules else 0.0

        alert_message = "; ".join(alerts) if alerts else None

        return WildfireDecision(
            risk_level=max_risk_level,
            alert_message=alert_message,
            confidence=confidence,
            triggered_rules=triggered_rules,
            timestamp=datetime.now(),
        )


class SimpleReflexAgent:
    """Simple Reflex Agent for Wildfire Detection"""

    def __init__(self, rapidapi_key: Optional[str] = None):
        self.location_services = LocationServices(rapidapi_key)
        self.rule_engine = RuleEngine()
        self._setup_default_rules()

        # Configuration thresholds
        self.thermal_threshold = float(os.getenv("THERMAL_THRESHOLD", "330"))
        self.humidity_threshold = float(os.getenv("HUMIDITY_THRESHOLD", "30"))
        self.wind_threshold = float(os.getenv("WIND_SPEED_THRESHOLD", "15"))

        logger.info("SimpleReflexAgent initialized")

    def _setup_default_rules(self):
        """Setup default wildfire detection rules"""

        @self.rule_engine.add_rule("high_temperature_forest")
        def high_temperature_forest_rule(
            percepts: EnvironmentalPercepts,
        ) -> Optional[str]:
            if (
                percepts.thermal > self.thermal_threshold
                and percepts.landuse == "forest"
                and percepts.humidity < self.humidity_threshold
            ):
                return "🔥 CRITICAL wildfire risk: High temperature in forest with low humidity"
            return None

        @self.rule_engine.add_rule("extreme_weather")
        def extreme_weather_rule(percepts: EnvironmentalPercepts) -> Optional[str]:
            if (
                percepts.wind_speed > self.wind_threshold
                and percepts.humidity < 20
                and percepts.thermal > 315
            ):
                return "⚠️ HIGH wildfire risk: Extreme weather conditions"
            return None

        @self.rule_engine.add_rule("vegetation_thermal")
        def vegetation_thermal_rule(percepts: EnvironmentalPercepts) -> Optional[str]:
            if (
                percepts.vegetation_density > 0.6
                and percepts.thermal > 325
                and percepts.humidity < 40
            ):
                return (
                    "🌲 HIGH wildfire risk: Dense vegetation with elevated temperature"
                )
            return None

        @self.rule_engine.add_rule("asset_proximity")
        def asset_proximity_rule(percepts: EnvironmentalPercepts) -> Optional[str]:
            if (
                percepts.asset_proximity < 5.0
                and percepts.thermal > 315
                and percepts.landuse in ["forest", "grassland"]
            ):
                return "🏘️ MEDIUM wildfire risk: Potential threat to nearby assets"
            return None

    def perceive(self, lat: float, lon: float) -> EnvironmentalPercepts:
        """Perceive environmental conditions at given location"""
        logger.info(f"Perceiving environmental data at ({lat}, {lon})")

        try:
            thermal = self.location_services.get_thermal_data(lat, lon)
            land_cover = self.location_services.get_land_cover(lat, lon)
            weather = self.location_services.get_weather_data(lat, lon)
            vegetation = self.location_services.get_vegetation_density(lat, lon)
            assets = self.location_services.get_asset_proximity(lat, lon)

            percepts = EnvironmentalPercepts(
                thermal=thermal,
                humidity=weather["humidity"],
                wind_speed=weather["wind_speed"],
                landuse=land_cover,
                vegetation_density=vegetation,
                asset_proximity=assets,
                timestamp=datetime.now(),
                latitude=lat,
                longitude=lon,
            )

            logger.info(
                f"Percepts gathered: thermal={thermal}K, humidity={weather['humidity']}%, landuse={land_cover}"
            )
            return percepts

        except Exception as e:
            logger.error(f"Error perceiving environmental data: {e}")
            raise

    def decide(self, percepts: EnvironmentalPercepts) -> WildfireDecision:
        """Apply rule engine to make decision"""
        logger.info("Evaluating percepts with rule engine")
        decision = self.rule_engine.evaluate(percepts)
        logger.info(
            f"Decision: {decision.risk_level} risk, {len(decision.triggered_rules)} rules triggered"
        )
        return decision

    def act(self, decision: WildfireDecision) -> None:
        """Take action based on decision"""
        if decision.alert_message:
            logger.warning(f"WILDFIRE ALERT: {decision.alert_message}")
            # In a real implementation, this could send notifications,
            # trigger emergency systems, etc.
        else:
            logger.info(f"No alerts. Risk level: {decision.risk_level}")

    def run(self, lat: float, lon: float) -> WildfireDecision:
        """Main agent execution cycle: perceive -> decide -> act"""
        logger.info(f"Running wildfire detection for location ({lat}, {lon})")

        # Perceive
        percepts = self.perceive(lat, lon)

        # Decide
        decision = self.decide(percepts)

        # Act
        self.act(decision)

        return decision

    def add_rule(self, name: str = None):
        """Add custom rule to the agent"""
        return self.rule_engine.add_rule(name)


# Example usage
if __name__ == "__main__":
    # Initialize agent
    agent = SimpleReflexAgent()

    # Test locations
    test_locations = [
        (34.0522, -118.2437),  # Los Angeles
        (37.7749, -122.4194),  # San Francisco
        (45.5152, -122.6784),  # Portland
    ]

    for lat, lon in test_locations:
        print(f"\n--- Testing location: ({lat}, {lon}) ---")
        result = agent.run(lat, lon)
        print(f"Risk Level: {result.risk_level}")
        print(f"Confidence: {result.confidence:.2f}")
        if result.alert_message:
            print(f"Alert: {result.alert_message}")
        print(
            f"Triggered Rules: {', '.join(result.triggered_rules) if result.triggered_rules else 'None'}"
        )
