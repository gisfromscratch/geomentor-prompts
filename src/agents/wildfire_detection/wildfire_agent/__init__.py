"""
Wildfire Detection Agent Module

This module provides a simple reflex agent for wildfire detection based on
environmental percepts and condition-action rules.
"""

from wildfire_agent.agent import (
    SimpleReflexAgent,
    EnvironmentalPercepts,
    WildfireDecision,
    RuleEngine,
)
from wildfire_agent.location import LocationServices

__all__ = [
    "SimpleReflexAgent",
    "EnvironmentalPercepts", 
    "WildfireDecision",
    "LocationServices",
    "RuleEngine",
]

__version__ = "1.0.0"
