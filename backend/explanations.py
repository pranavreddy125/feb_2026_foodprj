"""
Personality determination and explanation generation.
Episode: cursor_foodapp
"""

from typing import List, Set
from .taste_vector import UserTasteVector, FoodDistance, PersonalityProfile, ComfortRingAssignment
from .archetypes import Archetype
from .food_data import FOODS, DIMENSION_NAMES


def determine_personality(
    user_vector: UserTasteVector,
    archetypes: Set[Archetype],
    ring_0: List[FoodDistance],
    ring_1: List[FoodDistance],
    ring_2: List[FoodDistance]
) -> PersonalityProfile:
    """
    Determine primary and secondary food personality based on:
    - User taste vector dominant dimensions
    - Archetypes
    - Ring distribution
    """
    vec = user_vector.to_tuple()
    
    # Define personality types based on dominant dimensions
    personalities = {
        "Comfort Seeker": vec[2] <= 0.2 and vec[4] <= 0.2,
        "Spice Lover": vec[0] >= 0.8,
        "Texture Explorer": vec[1] >= 0.8,
        "Adventurous Eater": vec[4] >= 0.8,
        "Minimalist": vec[3] <= 0.2 and sum(vec) < 2.0,
        "Balanced Eater": all(0.4 <= v <= 0.6 for v in vec),
        "Rich Food Lover": vec[3] >= 0.8,
        "Familiar First": vec[2] <= 0.2,
        "Global Palate": vec[2] >= 0.5 and vec[4] >= 0.5,
    }
    
    # Score personalities
    scores = {}
    for personality_name, matches in personalities.items():
        score = 1.0 if matches else 0.0
        
        # Bonus from archetypes
        if personality_name == "Texture Explorer" and Archetype.TEXTURE_AVOIDER not in archetypes:
            score += 0.2
        if personality_name == "Spice Lover" and Archetype.HEAT_SEEKER in archetypes:
            score += 0.3
        if personality_name == "Comfort Seeker" and Archetype.COMFORT_MAXIMALIST in archetypes:
            score += 0.3
        if personality_name == "Adventurous Eater" and Archetype.FLAVOR_EXPLORER in archetypes:
            score += 0.3
        if personality_name == "Minimalist" and Archetype.REFINED_MINIMALIST in archetypes:
            score += 0.3
        
        # Bonus from ring distribution
        if personality_name == "Comfort Seeker" and len(ring_0) > len(ring_2):
            score += 0.2
        if personality_name == "Adventurous Eater" and len(ring_2) > len(ring_0):
            score += 0.2
        
        scores[personality_name] = score
    
    # Get top 2
    sorted_personalities = sorted(scores.items(), key=lambda x: (-x[1], x[0]))
    
    primary = sorted_personalities[0]
    secondary = sorted_personalities[1] if len(sorted_personalities) > 1 else ("Unknown", 0.0)
    
    # Normalize confidence
    total_score = sum(s for _, s in sorted_personalities)
    confidence_primary = primary[1] / total_score if total_score > 0 else 0.0
    confidence_secondary = secondary[1] / total_score if total_score > 0 else 0.0
    
    # Generate explanation
    explanation = generate_personality_explanation(
        primary[0], user_vector, archetypes, ring_0, ring_1, ring_2
    )
    
    return PersonalityProfile(
        primary_personality=primary[0],
        secondary_personality=secondary[0],
        confidence_primary=min(confidence_primary, 1.0),
        confidence_secondary=min(confidence_secondary, 1.0),
        explanation=explanation
    )


def generate_personality_explanation(
    personality: str,
    user_vector: UserTasteVector,
    archetypes: Set[Archetype],
    ring_0: List[FoodDistance],
    ring_1: List[FoodDistance],
    ring_2: List[FoodDistance]
) -> str:
    """Generate truthful explanation for personality assignment."""
    vec = user_vector.to_tuple()
    
    reasons = []
    
    # Dimension-based reasons
    if personality == "Comfort Seeker":
        reasons.append(f"Your preparation familiarity preference is {vec[2]} (low)")
        reasons.append(f"Your psychological distance tolerance is {vec[4]} (low)")
        reasons.append(f"Ring 0 contains {len(ring_0)} foods (comfort zone)")
    
    elif personality == "Spice Lover":
        reasons.append(f"Your spice intensity preference is {vec[0]} (high)")
    
    elif personality == "Texture Explorer":
        reasons.append(f"Your texture intensity preference is {vec[1]} (high)")
    
    elif personality == "Adventurous Eater":
        reasons.append(f"Your psychological distance tolerance is {vec[4]} (high)")
        reasons.append(f"Ring 2 contains {len(ring_2)} foods (experimental zone)")
    
    elif personality == "Minimalist":
        reasons.append(f"Your richness preference is {vec[3]} (low)")
        reasons.append(f"Overall taste vector sum is {sum(vec):.2f} (restrained)")
    
    elif personality == "Balanced Eater":
        reasons.append("All dimensions fall in moderate range [0.4-0.6]")
    
    elif personality == "Rich Food Lover":
        reasons.append(f"Your richness preference is {vec[3]} (high)")
    
    elif personality == "Familiar First":
        reasons.append(f"Your preparation familiarity preference is {vec[2]} (low, prefer familiar)")
    
    elif personality == "Global Palate":
        reasons.append(f"Your preparation familiarity is {vec[2]} (high)")
        reasons.append(f"Your psychological distance tolerance is {vec[4]} (high)")
    
    # Archetype influences
    for archetype in archetypes:
        reasons.append(f"Archetype: {archetype.value}")
    
    return " | ".join(reasons)


def explain_ring_assignment(assignment: ComfortRingAssignment) -> str:
    """Generate human-readable explanation of ring assignments."""
    lines = []
    lines.append("=" * 80)
    lines.append("FOOD PERSONALITY & COMFORT RING ASSIGNMENT")
    lines.append("=" * 80)
    lines.append("")
    
    # User vector
    lines.append("USER TASTE VECTOR:")
    vec = assignment.user_vector
    lines.append(f"  Spice Intensity: {vec.spice_intensity}")
    lines.append(f"  Texture Intensity: {vec.texture_intensity}")
    lines.append(f"  Preparation Familiarity: {vec.preparation_familiarity}")
    lines.append(f"  Richness: {vec.richness}")
    lines.append(f"  Psychological Distance: {vec.psychological_distance}")
    lines.append("")
    
    # Dislikes
    if assignment.dislikes:
        lines.append(f"DISLIKES: {', '.join(sorted(assignment.dislikes))}")
        lines.append("")
    
    # Archetypes
    if assignment.archetypes:
        lines.append("ARCHETYPES:")
        for archetype in sorted(assignment.archetypes, key=lambda a: a.value):
            lines.append(f"  - {archetype.value}")
        lines.append("")
    
    # Ring thresholds
    t0, t1 = assignment.ring_thresholds
    lines.append("RING THRESHOLDS:")
    lines.append(f"  Ring 0 (Core Comfort): distance ≤ {t0:.3f}")
    lines.append(f"  Ring 1 (Safe Stretch): {t0:.3f} < distance ≤ {t1:.3f}")
    lines.append(f"  Ring 2 (Experimental): distance > {t1:.3f}")
    lines.append("")
    
    # Personality
    p = assignment.personality
    lines.append("FOOD PERSONALITY:")
    lines.append(f"  Primary: {p.primary_personality} (confidence: {p.confidence_primary:.2%})")
    lines.append(f"  Secondary: {p.secondary_personality} (confidence: {p.confidence_secondary:.2%})")
    lines.append(f"  Explanation: {p.explanation}")
    lines.append("")
    
    # Rings
    for ring_num, ring_foods, ring_name in [
        (0, assignment.ring_0, "RING 0 — Core Comfort"),
        (1, assignment.ring_1, "RING 1 — Adjacent / Safe Stretch"),
        (2, assignment.ring_2, "RING 2 — Far Edge / Experimental")
    ]:
        lines.append("=" * 80)
        lines.append(f"{ring_name} ({len(ring_foods)} foods)")
        lines.append("=" * 80)
        for fd in ring_foods:
            lines.append(f"  {fd.food_name:<30} distance: {fd.distance:.3f}")
        lines.append("")
    
    return "\n".join(lines)


def explain_food_distance(
    food_name: str,
    assignment: ComfortRingAssignment
) -> str:
    """Generate detailed explanation for why a specific food is in its ring."""
    # Find food
    all_foods = assignment.ring_0 + assignment.ring_1 + assignment.ring_2
    food_dist = None
    for fd in all_foods:
        if fd.food_name == food_name:
            food_dist = fd
            break
    
    if not food_dist:
        return f"Food '{food_name}' not found."
    
    lines = []
    lines.append("=" * 80)
    lines.append(f"DETAILED EXPLANATION: {food_name}")
    lines.append("=" * 80)
    lines.append("")
    
    lines.append(f"Ring: {food_dist.ring}")
    lines.append(f"Total Distance: {food_dist.distance:.3f}")
    lines.append("")
    
    lines.append("DIMENSION CONTRIBUTIONS:")
    for dim, contrib in sorted(food_dist.dimension_contributions.items()):
        lines.append(f"  {dim:<30} {contrib:.4f}")
    lines.append("")
    
    # Show food vector vs user vector
    food_vec = FOODS[food_name]
    user_vec = assignment.user_vector.to_tuple()
    lines.append("DIMENSION-BY-DIMENSION COMPARISON:")
    for i, dim_name in enumerate(DIMENSION_NAMES):
        lines.append(f"  {dim_name:<30} User: {user_vec[i]:.1f}  Food: {food_vec[i]:.1f}  Diff: {abs(user_vec[i] - food_vec[i]):.1f}")
    lines.append("")
    
    return "\n".join(lines)
