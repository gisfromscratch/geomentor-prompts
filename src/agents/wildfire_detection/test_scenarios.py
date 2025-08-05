#!/usr/bin/env python3
"""
Test script to demonstrate wildfire detection with various risk scenarios
"""

from wildfire_agent import SimpleReflexAgent, EnvironmentalPercepts
from datetime import datetime
from zoneinfo import ZoneInfo


def test_high_risk_scenarios():
    """Test the agent with various high-risk scenarios"""
    print("🔥 Testing High-Risk Wildfire Scenarios")
    print("=" * 50)

    agent = SimpleReflexAgent()

    # Define test scenarios with different risk levels
    scenarios = [
        {
            "name": "California Wildfire Season",
            "percepts": EnvironmentalPercepts(
                thermal=335.0,  # High temperature (above 330K threshold)
                humidity=15.0,  # Very low humidity (below 30% threshold)
                wind_speed=25.0,  # High wind speed (above 15 km/h threshold)
                landuse="forest",  # Forest land use
                vegetation_density=0.9,  # Dense vegetation
                asset_proximity=3.0,  # Close to assets
                timestamp=datetime.now(),
                latitude=34.0522,
                longitude=-118.2437,
            ),
        },
        {
            "name": "Moderate Grassland Risk",
            "percepts": EnvironmentalPercepts(
                thermal=320.0,
                humidity=25.0,  # Low humidity
                wind_speed=18.0,  # High wind
                landuse="grassland",
                vegetation_density=0.5,
                asset_proximity=2.0,  # Very close to assets
                timestamp=datetime.now(),
                latitude=39.7392,
                longitude=-104.9903,
            ),
        },
        {
            "name": "Dense Forest High Temperature",
            "percepts": EnvironmentalPercepts(
                thermal=328.0,  # High temperature
                humidity=25.0,  # Low humidity
                wind_speed=10.0,  # Moderate wind
                landuse="forest",
                vegetation_density=0.8,  # Dense vegetation
                asset_proximity=12.0,  # Distant from assets
                timestamp=datetime.now(),
                latitude=45.5152,
                longitude=-122.6784,
            ),
        },
        {
            "name": "Urban Low Risk",
            "percepts": EnvironmentalPercepts(
                thermal=295.0,  # Normal temperature
                humidity=60.0,  # High humidity
                wind_speed=8.0,  # Low wind
                landuse="urban",
                vegetation_density=0.2,  # Low vegetation
                asset_proximity=1.0,  # Very close to assets
                timestamp=datetime.now(),
                latitude=37.7749,
                longitude=-122.4194,
            ),
        },
        {
            "name": "Canadian Wildfire SS027-25",
            "percepts": EnvironmentalPercepts(
                thermal=294.0,
                humidity=82.0,
                wind_speed=6.4,
                landuse="rangeland",
                vegetation_density=0.63,
                asset_proximity=30.0,
                timestamp=datetime(2025, 8, 4, 22, 47, 0, tzinfo=ZoneInfo("America/Inuvik")),
                latitude=61.291,
                longitude=-112.821,
            ),
        }
    ]

    for i, scenario in enumerate(scenarios, 1):
        print(f"\n🎭 Scenario {i}: {scenario['name']}")
        print("-" * 40)

        percepts = scenario["percepts"]

        # Display percepts
        print(f"📊 Environmental Conditions:")
        print(f"   Temperature: {percepts.thermal}K")
        print(f"   Humidity: {percepts.humidity}%")
        print(f"   Wind Speed: {percepts.wind_speed} km/h")
        print(f"   Land Use: {percepts.landuse}")
        print(f"   Vegetation Density: {percepts.vegetation_density}")
        print(f"   Asset Proximity: {percepts.asset_proximity} km")

        # Make decision using the rule engine
        decision = agent.decide(percepts)

        # Take action
        agent.act(decision)

        # Display results
        risk_emoji = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🟠", "CRITICAL": "🔴"}

        print(f"\n📋 Risk Assessment:")
        print(
            f"   Risk Level: {risk_emoji.get(decision.risk_level, '⚪')} {decision.risk_level}"
        )
        print(f"   Confidence: {decision.confidence:.2f}")

        if decision.alert_message:
            print(f"   Alert: {decision.alert_message}")
        else:
            print("   Alert: No immediate threats detected")

        if decision.triggered_rules:
            print(f"   Triggered Rules: {', '.join(decision.triggered_rules)}")
        else:
            print("   Triggered Rules: None")


def test_custom_rule():
    """Test adding a custom rule to the agent"""
    print("\n\n🛠️ Testing Custom Rule Addition")
    print("=" * 50)

    agent = SimpleReflexAgent()

    # Add a custom rule for drought conditions
    @agent.add_rule("drought_conditions")
    def drought_rule(percepts):
        if (
            percepts.humidity < 15
            and percepts.vegetation_density > 0.3
            and percepts.thermal > 300
        ):
            return "🌵 MEDIUM wildfire risk: Drought conditions detected"
        return None

    # Test the custom rule
    test_percepts = EnvironmentalPercepts(
        thermal=310.0,
        humidity=12.0,  # Very low humidity (drought)
        wind_speed=10.0,
        landuse="grassland",
        vegetation_density=0.4,  # Some vegetation
        asset_proximity=8.0,
        timestamp=datetime.now(),
        latitude=35.0,
        longitude=-115.0,
    )

    print("📊 Testing custom drought rule with percepts:")
    print(f"   Temperature: {test_percepts.thermal}K")
    print(f"   Humidity: {test_percepts.humidity}%")
    print(f"   Vegetation Density: {test_percepts.vegetation_density}")

    decision = agent.decide(test_percepts)
    agent.act(decision)

    print(f"\n📋 Result:")
    print(f"   Risk Level: {decision.risk_level}")
    print(f"   Alert: {decision.alert_message}")
    print(f"   Triggered Rules: {', '.join(decision.triggered_rules)}")


if __name__ == "__main__":
    test_high_risk_scenarios()
    test_custom_rule()