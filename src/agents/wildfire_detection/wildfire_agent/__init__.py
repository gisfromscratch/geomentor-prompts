"""
Wildfire Detection Agent Module

This module provides a simple reflex agent for wildfire detection based on
environmental percepts and condition-action rules.
"""

from .agent import (
    SimpleReflexAgent,
    EnvironmentalPercepts,
    WildfireDecision,
    LocationServices,
    RuleEngine,
)

__all__ = [
    "SimpleReflexAgent",
    "EnvironmentalPercepts", 
    "WildfireDecision",
    "LocationServices",
    "RuleEngine",
]

__version__ = "1.0.0"
