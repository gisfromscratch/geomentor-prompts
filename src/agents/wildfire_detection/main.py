#!/usr/bin/env python3
"""
Main entry point for the Simple Reflex Agent for Wildfire Detection
"""

from wildfire_agent import SimpleReflexAgent


def main():
    """Main function to demonstrate the wildfire detection agent"""
    print("🔥 Simple Reflex Agent for Wildfire Detection")
    print("=" * 50)

    # Initialize agent
    agent = SimpleReflexAgent()

    # Test locations with varying risk profiles
    test_locations = [
        (34.0522, -118.2437, "Los Angeles, CA"),
        (37.7749, -122.4194, "San Francisco, CA"),
        (45.5152, -122.6784, "Portland, OR"),
        (39.7392, -104.9903, "Denver, CO"),
    ]

    print(f"\nTesting {len(test_locations)} locations for wildfire risk...\n")

    for lat, lon, location_name in test_locations:
        print(f"📍 {location_name} ({lat}, {lon})")
        print("-" * 40)

        try:
            result = agent.run(lat, lon)

            # Display results
            risk_emoji = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🟠", "CRITICAL": "🔴"}

            print(
                f"Risk Level: {risk_emoji.get(result.risk_level, '⚪')} {result.risk_level}"
            )
            print(f"Confidence: {result.confidence:.2f}")

            if result.alert_message:
                print(f"Alert: {result.alert_message}")
            else:
                print("Alert: No immediate threats detected")

            if result.triggered_rules:
                print(f"Triggered Rules: {', '.join(result.triggered_rules)}")
            else:
                print("Triggered Rules: None")

        except Exception as e:
            print(f"❌ Error processing location: {e}")

        print()


if __name__ == "__main__":
    main()
