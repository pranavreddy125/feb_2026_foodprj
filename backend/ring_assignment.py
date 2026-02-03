"""
Ring assignment logic.
Episode: cursor_foodapp
"""

from typing import List, Set, Tuple
from .taste_vector import UserTasteVector, FoodDistance, ComfortRingAssignment
from .archetypes import Archetype
from .food_data import FOODS
from .distance import compute_distance_with_archetypes
from .explanations import determine_personality


def compute_ring_thresholds(
    distances: List[float],
    archetypes: Set[Archetype]
) -> Tuple[float, float]:
    """
    Compute ring thresholds based on distance distribution and archetypes.
    
    Base: use percentiles (33rd, 66th)
    Archetypes adjust thresholds:
    - Comfort Maximalist: compresses Ring 0 (lowers threshold_0)
    - Flavor Explorer: expands Ring 1 (raises threshold_1)
    
    Returns: (threshold_0, threshold_1) where:
        - distance <= threshold_0 → Ring 0
        - threshold_0 < distance <= threshold_1 → Ring 1
        - distance > threshold_1 → Ring 2
    """
    sorted_distances = sorted(distances)
    n = len(sorted_distances)
    
    # Base thresholds: 33rd and 66th percentiles
    idx_33 = int(n * 0.33)
    idx_66 = int(n * 0.66)
    
    threshold_0 = sorted_distances[idx_33] if idx_33 < n else sorted_distances[-1]
    threshold_1 = sorted_distances[idx_66] if idx_66 < n else sorted_distances[-1]
    
    # Archetype adjustments
    if Archetype.COMFORT_MAXIMALIST in archetypes:
        # Compress Ring 0 (make it smaller, stricter)
        threshold_0 *= 0.8
    
    if Archetype.FLAVOR_EXPLORER in archetypes:
        # Expand Ring 1 (make it larger)
        threshold_1 *= 1.2
    
    # Ensure monotonicity: threshold_0 < threshold_1
    if threshold_0 >= threshold_1:
        threshold_1 = threshold_0 + 0.01
    
    return (threshold_0, threshold_1)


def assign_to_rings(
    user_vector: UserTasteVector,
    dislikes: Set[str],
    archetypes: Set[Archetype]
) -> ComfortRingAssignment:
    """
    Main function: assign all foods to rings.
    
    Process:
    1. Validate user vector
    2. Compute distances to all foods with archetype adjustments
    3. Determine ring thresholds
    4. Assign foods to rings (ensuring partition completeness I3)
    5. Determine personality
    """
    user_vector.validate()
    user_vec = user_vector.to_tuple()
    
    # Compute distances
    food_distances = []
    all_distances = []
    
    for food_name, food_vec in FOODS.items():
        distance, dim_contrib = compute_distance_with_archetypes(
            user_vec, food_vec, food_name, dislikes, archetypes
        )
        food_distances.append(FoodDistance(
            food_name=food_name,
            distance=distance,
            ring=-1,  # assigned later
            dimension_contributions=dim_contrib
        ))
        all_distances.append(distance)
    
    # Compute ring thresholds
    threshold_0, threshold_1 = compute_ring_thresholds(all_distances, archetypes)
    
    # Assign rings (I2: ring ordering, I3: partition completeness)
    ring_0 = []
    ring_1 = []
    ring_2 = []
    
    for fd in food_distances:
        if fd.distance <= threshold_0:
            fd.ring = 0
            ring_0.append(fd)
        elif fd.distance <= threshold_1:
            fd.ring = 1
            ring_1.append(fd)
        else:
            fd.ring = 2
            ring_2.append(fd)
    
    # Sort within rings by distance (monotonicity I2)
    ring_0.sort()
    ring_1.sort()
    ring_2.sort()
    
    # Determine personality
    personality = determine_personality(user_vector, archetypes, ring_0, ring_1, ring_2)
    
    return ComfortRingAssignment(
        user_vector=user_vector,
        dislikes=dislikes,
        archetypes=archetypes,
        ring_0=ring_0,
        ring_1=ring_1,
        ring_2=ring_2,
        personality=personality,
        ring_thresholds=(threshold_0, threshold_1)
    )
