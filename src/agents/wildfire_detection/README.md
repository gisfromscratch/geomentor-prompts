# 🔥 Simple Reflex Agent for Wildfire Detection

A **Simple Reflex Agent** implementation that detects wildfire risk based on real-time environmental percepts and triggers alerts using condition-action rules.

## 🎯 Overview

This agent represents the first implementation in our 4×3 design matrix for structured GeoAI reasoning. It uses a reactive approach to wildfire detection by:

1. **Perceiving** environmental conditions (thermal data, land cover, weather)
2. **Deciding** based on predefined condition-action rules
3. **Acting** by logging alerts or triggering notifications

## 🚀 Features

- **Real-time Environmental Monitoring**: Fetches thermal anomalies, land cover, and weather data
- **Rule-based Decision Making**: Custom rule engine for wildfire risk assessment
- **Configurable Thresholds**: Adjustable parameters for different risk scenarios
- **Location Services Integration**: Wrapper for geospatial data APIs

## 📋 Prerequisites

- Python 3.12+
- RapidAPI account for environmental data access
- UV package manager

## 🛠️ Installation

1. Install dependencies:
```bash
uv sync
```

2. Copy environment configuration:
```bash
cp .env.example .env
```

3. Configure your API keys in `.env`:
```bash
RAPIDAPI_KEY=your_rapidapi_key_here
```

## 💻 Usage

### Basic Example

```python
from wildfire_agent import SimpleReflexAgent

# Initialize agent
agent = SimpleReflexAgent()

# Monitor a location
lat, lon = 40.7128, -74.0060  # New York City
result = agent.run(lat, lon)

print(f"Risk Level: {result.risk_level}")
print(f"Alert: {result.alert_message}")
```

### Custom Rules

```python
# Add custom detection rule
@agent.add_rule
def high_temperature_forest_rule(percepts):
    if (percepts.thermal > 330 and 
        percepts.landuse == "forest" and 
        percepts.humidity < 30):
        return "🔥 High wildfire risk detected"
    return None
```

## 🧪 Testing

Run tests with:
```bash
uv --directory src/agents/wildfire_detection run test_scenarios.py
```

## 📊 Data Sources

- **Thermal Data**: MODIS thermal anomalies
- **Land Cover**: Classification data
- **Weather**: Humidity, wind speed, temperature
- **Assets**: Villages, roads, biodiversity hotspots proximity

## 🎛️ Configuration

Key parameters in `.env`:
- `THERMAL_THRESHOLD`: Temperature threshold for risk detection (default: 330K)
- `HUMIDITY_THRESHOLD`: Humidity percentage threshold (default: 30%)
- `WIND_SPEED_THRESHOLD`: Wind speed threshold in km/h (default: 15)

## 🔧 Architecture

```
SimpleReflexAgent
├── perceive(lat, lon) → Environmental data
├── decide(percepts) → Rule engine evaluation
└── act(decision) → Alert/logging action
```

## 📈 Roadmap

- [ ] Integration with real-time satellite feeds
- [ ] Machine learning rule optimization
- [ ] Multi-agent coordination
- [ ] Web dashboard interface