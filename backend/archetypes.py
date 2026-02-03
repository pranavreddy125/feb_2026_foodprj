"""
User archetypes that modify ring thresholds.
Episode: cursor_foodapp
"""

from enum import Enum


class Archetype(Enum):
    """User archetypes that modify ring thresholds."""
    TEXTURE_AVOIDER = "texture_avoider"
    HEAT_SEEKER = "heat_seeker"
    COMFORT_MAXIMALIST = "comfort_maximalist"
    FLAVOR_EXPLORER = "flavor_explorer"
    REFINED_MINIMALIST = "refined_minimalist"
