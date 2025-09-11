# 🛣️ Routing Agent: Bonn to Remagen Problem Solver

A **Problem-Solving Agent** implementation that models routing from Bonn to Remagen as an agentic task using the **ArcGIS Location Platform**. This agent follows the structured problem formulation approach with explicit state representation, actions, and goal testing.

## 🎯 Overview

This agent represents a prototype implementation of problem-solving in GeoAI, specifically demonstrating:

1. **Initial State**: Start location in Bonn (geocoded coordinates)
2. **Actions**: Movement along road network segments 
3. **Transition Model**: ArcGIS routing API computes new states and path costs
4. **Goal Test**: Check if current position is within buffer distance of Remagen
5. **Path Cost**: Travel time (primary metric) with multi-criteria extension capability

## 🚀 Features

- **ArcGIS Location Platform Integration**: Full integration with ArcGIS services
- **Geocoding Services**: Convert addresses to precise coordinates
- **Route Computation**: Compute optimal routes with detailed segments  
- **Goal Testing**: Buffer-based destination validation
- **Multi-criteria Path Costs**: Travel time, distance, and extensible cost functions
- **Feature Layer Publishing**: Export routes to ArcGIS Online for inspection
- **Comprehensive Validation**: Route and coordinate validation

## 📋 Prerequisites

- Python 3.12+
- ArcGIS API for Python (`pip install arcgis`)
- Valid ArcGIS credentials (username/password or API key)
- Active ArcGIS Location Platform subscription

## 🛠️ Installation

1. Install dependencies:
```bash
cd src/agents/routing_agent
pip install -e .
```

2. Copy environment configuration:
```bash
cp .env.example .env
```

3. Configure your ArcGIS credentials in `.env`:
```bash
# Username/Password authentication
ARCGIS_USERNAME=your_username
ARCGIS_PASSWORD=your_password

# OR API key authentication (recommended)
ARCGIS_API_KEY=your_api_key

# Optional configuration
ARCGIS_ORG_URL=https://www.arcgis.com
DEFAULT_TRAVEL_MODE=Driving
ROUTE_BUFFER_METERS=200
LOG_LEVEL=INFO
```

## 💻 Usage

### Basic Example

```python
from routing_agent import RoutingAgent

# Initialize agent with ArcGIS credentials
agent = RoutingAgent()

# Solve the Bonn to Remagen problem
result = agent.solve_routing_problem(
    start_address="Bonn, Germany",
    end_address="Remagen, Germany"
)

print(f"Route found: {result.summary()}")
print(f"Total time: {result.path_cost:.2f} minutes")
print(f"Distance: {result.total_distance:.2f} km")
```

### Advanced Usage

```python
# Custom locations
result = agent.solve_routing_problem(
    start_address="Köln, Germany",
    end_address="Düsseldorf, Germany"
)

# Multi-criteria cost analysis
time_heavy_cost = result.get_multi_criteria_cost(
    time_weight=0.8, distance_weight=0.2
)

# Validate the routing decision
is_valid = agent.validate_decision(result)

# Publish route to ArcGIS Online
feature_url = agent.publish_route_to_feature_layer(result)
```

### Problem Formulation Components

```python
# 1. Initial State (Geocoding)
start_state = agent.geocode_location("Bonn, Germany")

# 2. Goal State (Geocoding)
goal_state = agent.geocode_location("Remagen, Germany")

# 3. Transition Model (Route Computation)
routing_decision = agent.compute_route(start_state, goal_state)

# 4. Goal Test (Buffer Check)
goal_reached = agent.goal_test(start_state, goal_state)

# 5. Path Cost Analysis
primary_cost = routing_decision.path_cost
multi_cost = routing_decision.get_multi_criteria_cost()
```

## 🔬 Testing & Demo

### Quick Start (No ArcGIS Required)
The agent includes a mock implementation for testing and demonstration:

```bash
cd src/agents/routing_agent

# Run main demo (uses mock agent if ArcGIS not available)
python main.py

# Run comprehensive test suite
python test_scenarios.py

# Test core functionality
python -c "from routing_agent import LocationState; print('Core classes working!')"
```

### With ArcGIS API for Python
```bash
# Install ArcGIS dependencies (requires valid license)
pip install arcgis

# Configure credentials in .env
cp .env.example .env
# Edit .env with your ArcGIS credentials

# Run with real ArcGIS services
python main.py
```

### Test Scenarios Include:
- ✅ Basic Bonn to Remagen routing
- ✅ Geocoding accuracy validation  
- ✅ Goal test functionality
- ✅ Path cost calculations
- ✅ Route validation
- ✅ Alternative location routing

## 📊 Data Sources & Services

- **Geocoding**: ArcGIS World Geocoding Service
- **Routing**: ArcGIS World Route Service
- **Travel Modes**: Driving, Walking, Trucking, etc.
- **Output**: Polyline geometries with detailed turn-by-turn directions

## 🎛️ Configuration

Key parameters in `.env`:
- `DEFAULT_TRAVEL_MODE`: Routing mode (default: "Driving")
- `ROUTE_BUFFER_METERS`: Goal test buffer distance (default: 200m)
- `LOG_LEVEL`: Logging verbosity (default: "INFO")

## 🔧 Architecture

```
RoutingAgent
├── geocode_location(address) → LocationState
├── compute_route(start, end) → RoutingDecision  
├── goal_test(current, target) → Boolean
├── solve_routing_problem() → Complete workflow
└── publish_route_to_feature_layer() → ArcGIS Online
```

### Core Classes

- **LocationState**: Represents a geographic location with coordinates
- **RouteSegment**: Individual route segment with cost and directions
- **RoutingDecision**: Complete routing solution with validation

## 📈 Problem Formulation Structure

| Component | Implementation |
|-----------|----------------|
| **Initial State** | Geocoded Bonn coordinates |
| **Goal State** | Geocoded Remagen coordinates |
| **Actions** | Road network segment movements |
| **Transition Model** | ArcGIS routing API calls |
| **Goal Test** | Coordinate buffer validation (200m) |
| **Path Cost** | Travel time (minutes) + distance (km) |

## 🔍 Validation & Output

The agent provides comprehensive validation:
- ✅ Coordinate bounds checking (-90 to 90 lat, -180 to 180 lon)
- ✅ Positive travel times and distances
- ✅ Route segment consistency
- ✅ Goal achievement verification

Output includes:
- 🗺️ Complete route with turn-by-turn directions
- 📊 Detailed cost analysis (time, distance, multi-criteria)
- 🌐 Published feature layer for ArcGIS Online inspection
- ✅ Validation results and confidence scores

## 🚦 Expected Results

For the Bonn → Remagen route:
- **Distance**: ~20-25 km (straight-line ~20km, actual roads ~24km)
- **Travel Time**: ~20-30 minutes (driving)
- **Route**: Primarily via A555 and B9 highways (with ArcGIS) or simplified estimation (mock)
- **Confidence**: >0.9 for successful routing

### Sample Output (Mock Agent):
```
🛣️  Routing Agent: Bonn to Remagen Problem Solver
Agent Type: Mock
Status: ✅ Goal reached - 1 segments, 23.8 min, 23.81 km (confidence: 0.90)
Primary Cost (Travel Time): 23.81 minutes
Distance: 23.81 km
Multi-criteria Cost: 7.42
```

## 🔬 Extensions & Future Work

- [ ] **Risk-based Routing**: Incorporate traffic, weather, and road condition risks
- [ ] **Multi-modal Transport**: Support for public transit, walking, cycling
- [ ] **Real-time Updates**: Dynamic route adjustment based on current conditions  
- [ ] **Batch Processing**: Multiple origin-destination pairs
- [ ] **Optimization Algorithms**: A*, Dijkstra integration for custom routing

## 📝 Example Output

```
🛣️  Routing Agent: Bonn to Remagen Problem Solver
============================================================

📡 Initializing Routing Agent with ArcGIS Location Platform...
✅ Agent initialized successfully

🔍 Solving routing problem: Bonn → Remagen
----------------------------------------

📊 ROUTING RESULTS
==============================
Status: ✅ Goal reached - 12 segments, 23.4 min, 21.8 km (confidence: 1.00)
Start: Bonn, DEU (50.737430, 7.098206)
Goal: Remagen, DEU (50.579163, 7.228142)

💰 PATH COST ANALYSIS
--------------------
Primary Cost (Travel Time): 23.40 minutes
Distance: 21.80 km
Multi-criteria Cost: 6.93

✅ VALIDATION
--------------
Route validation: ✅ PASSED
Goal test result: ✅ REACHED  
Confidence score: 1.00

🎯 PROBLEM FORMULATION SUMMARY
-----------------------------------
✓ Initial State: Bonn coordinates geocoded
✓ Goal State: Remagen coordinates geocoded
✓ Actions: Road network segments computed
✓ Transition Model: ArcGIS routing API applied  
✓ Goal Test: Buffer distance check executed
✓ Path Cost: Travel time calculated
✓ Results: Published to feature layer
```

## 🤝 Contributing

This implementation serves as a prototype for structured GeoAI problem solving. Contributions welcome for:
- Additional routing algorithms
- Extended cost functions
- Performance optimizations
- Test coverage improvements

## 📄 License

This project follows the same license as the parent repository.