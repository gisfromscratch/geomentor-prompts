"""
Simple Reflex Agent for Wildfire Detection

This module implements a condition-action rule based agent that detects
wildfire risk based on environmental percepts.
"""

import logging
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, UTC
from typing import Dict, List, Optional, Callable
from dotenv import load_dotenv
from wildfire_agent.location import LocationServices

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

    def perceive(self, lat: float, lon: float, 
                 max_thermal_age_hours: float = 6.0,
                 max_weather_age_hours: float = 12.0) -> EnvironmentalPercepts:
        """
        Perceive environmental conditions at given location
        
        Args:
            lat: Latitude coordinate
            lon: Longitude coordinate  
            max_thermal_age_hours: Maximum age for thermal data to be considered valid (default: 6 hours)
            max_weather_age_hours: Maximum age for weather data to be considered valid (default: 12 hours)
        """
        logger.info(f"Perceiving environmental data at ({lat}, {lon})")

        try:
            # Detect thermal anomalies, land cover, weather, vegetation density, and asset proximity
            # Get thermal data with global coverage is not available, so we mock it
            thermal = self.location_services.get_thermal_data(lat, lon)
            
            # Check for nearby thermal activity with time constraint
            thermal_nearby = self.location_services.get_thermal_activity_nearby(lat, lon)
            if (
                thermal_nearby
                and thermal_nearby["confidence"] > 0.5
                and thermal_nearby.get("acquisition")
            ):
                try:
                    acquisition_time = datetime.fromisoformat(thermal_nearby["acquisition"])
                except (ValueError, TypeError):
                    acquisition_time = None

                if acquisition_time and datetime.now(UTC) - acquisition_time <= timedelta(hours=max_thermal_age_hours):
                    thermal_threshold = float(os.getenv("THERMAL_THRESHOLD", "330"))
                    thermal = thermal_threshold
                    logger.info(
                        f"Using nearby thermal activity: confidence={thermal_nearby['confidence']:.2f}, "
                        f"detected {thermal_nearby.get('hours_since_detected', 'N/A')} hours ago"
                    )
                elif (
                    "hours_since_detected" in thermal_nearby
                    and thermal_nearby["hours_since_detected"] > max_thermal_age_hours
                ):
                    logger.info(
                        f"Ignoring stale thermal activity: {thermal_nearby['hours_since_detected']:.1f} hours old "
                        f"(max age: {max_thermal_age_hours} hours)"
                    )
            elif (
                thermal_nearby
                and "hours_since_detected" in thermal_nearby
                and thermal_nearby["hours_since_detected"] > max_thermal_age_hours
            ):
                logger.info(
                    f"Ignoring stale thermal activity: {thermal_nearby['hours_since_detected']:.1f} hours old "
                    f"(max age: {max_thermal_age_hours} hours)"
                )
            
            # Land cover data is relatively stable and doesn't need time constraints
            land_cover = self.location_services.get_land_cover(lat, lon)
            
            # Weather data should be recent for accurate fire risk assessment
            weather = self.location_services.get_weather_data(lat, lon)
            # Note: In a real implementation, you would check the timestamp of weather data
            # and reject data older than max_weather_age_hours
            
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

    def validate(self, percepts: EnvironmentalPercepts) -> bool:
        """Validate percepts before decision making - pre-filter guardrails"""
        logger.info("Validating percepts")
        
        # Check for None values in critical fields
        if (percepts.thermal is None or percepts.humidity is None or 
            percepts.wind_speed is None or percepts.vegetation_density is None or
            percepts.asset_proximity is None or percepts.landuse is None or
            percepts.latitude is None or percepts.longitude is None):
            logger.error("Missing required percepts")
            return False

        # Validate thermal temperature (realistic Earth surface temperatures in Kelvin)
        if percepts.thermal < 200 or percepts.thermal > 400:
            logger.error(f"Unrealistic thermal temperature: {percepts.thermal}K (valid range: 200-400K)")
            return False

        # Validate humidity percentage (0-100%)
        if percepts.humidity < 0 or percepts.humidity > 100:
            logger.error(f"Invalid humidity: {percepts.humidity}% (valid range: 0-100%)")
            return False

        # Validate wind speed (non-negative, realistic maximum)
        if percepts.wind_speed < 0 or percepts.wind_speed > 200:
            logger.error(f"Invalid wind speed: {percepts.wind_speed} km/h (valid range: 0-200 km/h)")
            return False

        # Validate vegetation density (0-1 index)
        if percepts.vegetation_density < 0 or percepts.vegetation_density > 1:
            logger.error(f"Invalid vegetation density: {percepts.vegetation_density} (valid range: 0-1)")
            return False

        # Validate asset proximity (non-negative distance)
        if percepts.asset_proximity < 0:
            logger.error(f"Invalid asset proximity: {percepts.asset_proximity} km (must be >= 0)")
            return False

        # Validate geographic coordinates
        if percepts.latitude < -90 or percepts.latitude > 90:
            logger.error(f"Invalid latitude: {percepts.latitude} (valid range: -90 to 90)")
            return False
        
        if percepts.longitude < -180 or percepts.longitude > 180:
            logger.error(f"Invalid longitude: {percepts.longitude} (valid range: -180 to 180)")
            return False

        # Validate landuse classification
        valid_landuses = {"urban", "forest", "grassland"}
        if percepts.landuse not in valid_landuses:
            logger.error(f"Invalid landuse: {percepts.landuse} (valid options: {valid_landuses})")
            return False
        
        return True

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

        # Validate
        if not self.validate(percepts):
            logger.error("Invalid percepts, aborting decision")
            return None

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
