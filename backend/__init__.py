"""
Food Personality Backend Package
Episode: cursor_foodapp → postvibereportmajorfixes_2026

Clean, modular backend for 3-ring comfort food system.
Now with centralized food registry and metadata.
"""

__version__ = "1.0.1"

from .taste_vector import UserTasteVector, FoodDistance, PersonalityProfile, ComfortRingAssignment
from .archetypes import Archetype
from .food_data import FOODS, DIMENSION_NAMES, VALID_VALUES
from .food_registry import (
    FOOD_REGISTRY,
    FoodProfile,
    validate_food_registry,
    get_food_metadata,
    list_all_foods
)
from .distance import euclidean_distance, compute_distance_with_archetypes
from .ring_assignment import assign_to_rings, compute_ring_thresholds
from .explanations import (
    determine_personality,
    generate_personality_explanation,
    explain_ring_assignment,
    explain_food_distance
)

__all__ = [
    "UserTasteVector",
    "FoodDistance",
    "PersonalityProfile",
    "ComfortRingAssignment",
    "Archetype",
    "FOODS",
    "DIMENSION_NAMES",
    "VALID_VALUES",
    "FOOD_REGISTRY",
    "FoodProfile",
    "validate_food_registry",
    "get_food_metadata",
    "list_all_foods",
    "euclidean_distance",
    "compute_distance_with_archetypes",
    "assign_to_rings",
    "compute_ring_thresholds",
    "determine_personality",
    "generate_personality_explanation",
    "explain_ring_assignment",
    "explain_food_distance",
]
