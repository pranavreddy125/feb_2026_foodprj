"""
Distance calculation with archetype adjustments.
Episode: cursor_foodapp
"""

import math
from typing import Dict, Set, Tuple
from .archetypes import Archetype
from .food_data import DIMENSION_NAMES


def euclidean_distance(vec1: Tuple[float, ...], vec2: Tuple[float, ...]) -> float:
    """
    Standard Euclidean distance metric.
    Satisfies: non-negativity, identity, symmetry, triangle inequality (I1).
    """
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec1, vec2)))


def compute_distance_with_archetypes(
    user_vec: Tuple[float, ...],
    food_vec: Tuple[float, ...],
    food_name: str,
    dislikes: Set[str],
    archetypes: Set[Archetype]
) -> Tuple[float, Dict[str, float]]:
    """
    Compute distance with archetype adjustments.
    
    Archetype effects:
    - Dislikes: always increase distance (add penalty)
    - Texture Avoider: penalize texture mismatches
    - Heat Seeker: reduce spice mismatch penalty
    - Refined Minimalist: penalize high richness
    
    Returns: (adjusted_distance, dimension_contributions)
    """
    # Base dimension-wise differences
    diffs = [(a - b) ** 2 for a, b in zip(user_vec, food_vec)]
    dim_contributions = {name: diff for name, diff in zip(DIMENSION_NAMES, diffs)}
    
    # Apply archetype adjustments
    adjusted_diffs = list(diffs)
    
    # Dislikes: add flat penalty
    if food_name in dislikes:
        penalty = 1.5
        adjusted_diffs = [d + penalty for d in adjusted_diffs]
        dim_contributions["dislike_penalty"] = penalty * len(adjusted_diffs)
    
    # Texture Avoider: amplify texture dimension mismatch
    if Archetype.TEXTURE_AVOIDER in archetypes:
        texture_idx = 1  # texture_intensity
        texture_penalty = diffs[texture_idx] * 0.5
        adjusted_diffs[texture_idx] += texture_penalty
        dim_contributions["texture_avoider_penalty"] = texture_penalty
    
    # Heat Seeker: reduce spice dimension mismatch
    if Archetype.HEAT_SEEKER in archetypes:
        spice_idx = 0  # spice_intensity
        spice_reduction = diffs[spice_idx] * 0.3
        adjusted_diffs[spice_idx] = max(0, adjusted_diffs[spice_idx] - spice_reduction)
        dim_contributions["heat_seeker_reduction"] = -spice_reduction
    
    # Refined Minimalist: penalize high richness
    if Archetype.REFINED_MINIMALIST in archetypes:
        richness_idx = 3  # richness
        if food_vec[richness_idx] >= 0.8:  # high richness
            richness_penalty = 0.4
            adjusted_diffs[richness_idx] += richness_penalty
            dim_contributions["refined_minimalist_penalty"] = richness_penalty
    
    distance = math.sqrt(sum(adjusted_diffs))
    return distance, dim_contributions
