"""
Distance calculation with archetype adjustments.
Episode: cursor_foodapp → postvibereportmajorfixes_2026

P0 Fix #3: Asymmetric distance for tolerance dimensions.
- Familiarity is a floor: no penalty for foods more familiar than user seeks
- Heat tolerance is directional: no penalty for foods milder than user tolerates
"""

import math
from typing import Dict, Set, Tuple
from .archetypes import Archetype
from .food_data import DIMENSION_NAMES

# Asymmetric damping factors for tolerance dimensions
# When food is LESS exotic/spicy/unfamiliar than user tolerance, reduce penalty dramatically
# These values are calibrated to ensure cultural anchors (pizza, burgers)
# stay in Ring 0/1 for adventurous users while preserving penalties for
# foods that EXCEED user tolerance
PSYCHOLOGICAL_DISTANCE_DAMPING = 0.05  # 95% reduction for overly familiar foods
SPICE_INTENSITY_DAMPING = 0.05  # 95% reduction for overly mild foods
PREPARATION_FAMILIARITY_DAMPING = 0.05  # 95% reduction for overly familiar preparations


def euclidean_distance(vec1: Tuple[float, ...], vec2: Tuple[float, ...]) -> float:
    """
    Standard Euclidean distance metric.
    Satisfies: non-negativity, identity, symmetry, triangle inequality (I1).
    
    NOTE: This is the symmetric baseline. For asymmetric tolerance-based
    distance, use compute_distance_with_archetypes().
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
    Compute distance with archetype adjustments and asymmetric tolerance logic.
    
    ASYMMETRIC TOLERANCE DIMENSIONS:
    - psychological_distance (dim 4): Familiarity is a FLOOR
      * If food is MORE familiar than user seeks (food < user): dampened penalty
      * If food is MORE exotic than user tolerates (food > user): full penalty
    
    - spice_intensity (dim 0): Heat tolerance is DIRECTIONAL
      * If food is MILDER than user tolerates (food < user): dampened penalty
      * If food is SPICIER than user tolerates (food > user): full penalty
    
    - preparation_familiarity (dim 2): Preparation methods are tolerance-based
      * If food uses MORE familiar prep than user seeks (food < user): dampened penalty
      * If food uses MORE unfamiliar prep than user tolerates (food > user): full penalty
    
    RATIONALE:
    - Adventurous users aren't penalized for encountering familiar foods (pizza)
    - Heat seekers aren't penalized for encountering mild foods
    - Adventurous eaters aren't penalized for familiar preparation methods
    - Conservative users ARE penalized for exotic foods (correct)
    - Heat avoiders ARE penalized for spicy foods (correct)
    - Traditional eaters ARE penalized for unfamiliar preparations (correct)
    
    Archetype effects:
    - Dislikes: always increase distance (add penalty)
    - Texture Avoider: penalize texture mismatches
    - Heat Seeker: reduce spice mismatch penalty (legacy, now redundant with asymmetry)
    - Refined Minimalist: penalize high richness
    
    Returns: (adjusted_distance, dimension_contributions)
    """
    # Dimension indices
    SPICE_IDX = 0
    TEXTURE_IDX = 1
    PREP_FAM_IDX = 2
    RICHNESS_IDX = 3
    PSYCH_DIST_IDX = 4
    
    # Base dimension-wise differences (BEFORE asymmetric adjustments)
    base_diffs = [(a - b) ** 2 for a, b in zip(user_vec, food_vec)]
    dim_contributions = {name: diff for name, diff in zip(DIMENSION_NAMES, base_diffs)}
    
    # Start with symmetric differences, then apply asymmetric adjustments
    adjusted_diffs = list(base_diffs)
    
    # === ASYMMETRIC TOLERANCE LOGIC ===
    
    # 1. Psychological Distance (Familiarity Floor)
    user_psych = user_vec[PSYCH_DIST_IDX]
    food_psych = food_vec[PSYCH_DIST_IDX]
    
    if food_psych < user_psych:
        # Food is MORE familiar than user seeks → dampen penalty
        # Example: Adventurous user (0.8) encountering pizza (0.2)
        original_penalty = base_diffs[PSYCH_DIST_IDX]
        dampened_penalty = original_penalty * PSYCHOLOGICAL_DISTANCE_DAMPING
        adjusted_diffs[PSYCH_DIST_IDX] = dampened_penalty
        dim_contributions["psychological_distance_damping"] = original_penalty - dampened_penalty
    # else: Food is MORE exotic than user tolerates → keep full penalty
    
    # 2. Spice Intensity (Heat Tolerance Directional)
    user_spice = user_vec[SPICE_IDX]
    food_spice = food_vec[SPICE_IDX]
    
    if food_spice < user_spice:
        # Food is MILDER than user tolerates → dampen penalty
        # Example: Heat seeker (0.8) encountering mild food (0.2)
        original_penalty = base_diffs[SPICE_IDX]
        dampened_penalty = original_penalty * SPICE_INTENSITY_DAMPING
        adjusted_diffs[SPICE_IDX] = dampened_penalty
        dim_contributions["spice_intensity_damping"] = original_penalty - dampened_penalty
    # else: Food is SPICIER than user tolerates → keep full penalty
    
    # 3. Preparation Familiarity (Method Tolerance)
    user_prep = user_vec[PREP_FAM_IDX]
    food_prep = food_vec[PREP_FAM_IDX]
    
    if food_prep < user_prep:
        # Food uses MORE familiar preparation than user seeks → dampen penalty
        # Example: Adventurous eater (0.5) encountering simple prep (0.2)
        original_penalty = base_diffs[PREP_FAM_IDX]
        dampened_penalty = original_penalty * PREPARATION_FAMILIARITY_DAMPING
        adjusted_diffs[PREP_FAM_IDX] = dampened_penalty
        dim_contributions["preparation_familiarity_damping"] = original_penalty - dampened_penalty
    # else: Food uses MORE unfamiliar prep than user tolerates → keep full penalty
    
    # === ARCHETYPE ADJUSTMENTS (Applied after asymmetric logic) ===
    
    # Dislikes: add flat penalty to all dimensions
    if food_name in dislikes:
        penalty = 1.5
        adjusted_diffs = [d + penalty for d in adjusted_diffs]
        dim_contributions["dislike_penalty"] = penalty * len(adjusted_diffs)
    
    # Texture Avoider: amplify texture dimension mismatch
    if Archetype.TEXTURE_AVOIDER in archetypes:
        texture_penalty = base_diffs[TEXTURE_IDX] * 0.5
        adjusted_diffs[TEXTURE_IDX] += texture_penalty
        dim_contributions["texture_avoider_penalty"] = texture_penalty
    
    # Heat Seeker: reduce spice dimension mismatch (legacy - now less impactful due to asymmetry)
    if Archetype.HEAT_SEEKER in archetypes:
        spice_reduction = base_diffs[SPICE_IDX] * 0.3
        adjusted_diffs[SPICE_IDX] = max(0, adjusted_diffs[SPICE_IDX] - spice_reduction)
        dim_contributions["heat_seeker_reduction"] = -spice_reduction
    
    # Refined Minimalist: penalize high richness
    if Archetype.REFINED_MINIMALIST in archetypes:
        if food_vec[RICHNESS_IDX] >= 0.8:  # high richness
            richness_penalty = 0.4
            adjusted_diffs[RICHNESS_IDX] += richness_penalty
            dim_contributions["refined_minimalist_penalty"] = richness_penalty
    
    distance = math.sqrt(sum(adjusted_diffs))
    return distance, dim_contributions
