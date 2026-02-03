"""
Food Personality Backend Package
Episode: cursor_foodapp

Clean, modular backend for 3-ring comfort food system.
"""

__version__ = "1.0.0"

from .taste_vector import UserTasteVector, FoodDistance, PersonalityProfile, ComfortRingAssignment
from .archetypes import Archetype
from .food_data import FOODS, DIMENSION_NAMES, VALID_VALUES
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
    "euclidean_distance",
    "compute_distance_with_archetypes",
    "assign_to_rings",
    "compute_ring_thresholds",
    "determine_personality",
    "generate_personality_explanation",
    "explain_ring_assignment",
    "explain_food_distance",
]
