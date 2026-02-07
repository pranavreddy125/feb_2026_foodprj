"""
Fixed food data for the system.
Episode: cursor_foodapp → postvibereportmajorfixes_2026

DEPRECATED: This file now imports from food_registry.py
All food data should be accessed via the FOOD_REGISTRY.

This file remains for backward compatibility only.
"""

# Import from the new centralized registry
from .food_registry import FOODS, DIMENSION_NAMES, VALID_VALUES, FOOD_REGISTRY

# Re-export for backward compatibility
__all__ = ["FOODS", "DIMENSION_NAMES", "VALID_VALUES", "FOOD_REGISTRY"]
