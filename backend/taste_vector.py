"""
Taste vector data structures.
Episode: cursor_foodapp
"""

from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
from .food_data import VALID_VALUES
from .archetypes import Archetype


@dataclass
class UserTasteVector:
    """User taste preferences as a 5-dimensional vector."""
    spice_intensity: float
    texture_intensity: float
    preparation_familiarity: float
    richness: float
    psychological_distance: float
    
    def to_tuple(self) -> Tuple[float, float, float, float, float]:
        return (
            self.spice_intensity,
            self.texture_intensity,
            self.preparation_familiarity,
            self.richness,
            self.psychological_distance
        )
    
    def validate(self):
        """Ensure all values are in valid set."""
        for val in self.to_tuple():
            if val not in VALID_VALUES:
                raise ValueError(f"Invalid value {val}, must be in {VALID_VALUES}")


@dataclass
class FoodDistance:
    """Distance calculation result for a food."""
    food_name: str
    distance: float
    ring: int
    dimension_contributions: Dict[str, float]
    
    def __lt__(self, other):
        """Sort by distance, then name for determinism."""
        if self.distance != other.distance:
            return self.distance < other.distance
        return self.food_name < other.food_name


@dataclass
class PersonalityProfile:
    """Complete personality analysis."""
    primary_personality: str
    secondary_personality: str
    confidence_primary: float
    confidence_secondary: float
    explanation: str


@dataclass
class ComfortRingAssignment:
    """Complete ring assignment with explanations."""
    user_vector: UserTasteVector
    dislikes: Set[str]
    archetypes: Set[Archetype]
    ring_0: List[FoodDistance]  # Core Comfort
    ring_1: List[FoodDistance]  # Adjacent / Safe Stretch
    ring_2: List[FoodDistance]  # Far Edge / Experimental
    personality: PersonalityProfile
    ring_thresholds: Tuple[float, float]  # (threshold_0, threshold_1)
