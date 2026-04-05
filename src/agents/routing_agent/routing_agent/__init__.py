"""
Routing Agent Package

This package implements a problem-solving agent for routing tasks using the
ArcGIS Location Platform, following the structured problem formulation approach.
"""

from .location_state import LocationState, RoutingDecision
from .mock_agent import MockRoutingAgent

__version__ = "0.1.0a"

# Import RoutingAgent conditionally to allow testing without ArcGIS
try:
    from .agent import RoutingAgent
    __all__ = ["RoutingAgent", "MockRoutingAgent", "LocationState", "RoutingDecision"]
except ImportError as e:
    # ArcGIS not available, only expose mock agent and location state classes
    __all__ = ["MockRoutingAgent", "LocationState", "RoutingDecision"]