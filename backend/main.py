#!/usr/bin/env python3
"""
Food Personality Backend - Main Entry Point
Episode: cursor_foodapp

Fixed system: 3 comfort rings, 5 semantic dimensions, 18 foods.
Deterministic, no ML, no embeddings, no external APIs.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import (
    UserTasteVector,
    Archetype,
    assign_to_rings,
    explain_ring_assignment,
    explain_food_distance
)


if __name__ == "__main__":
    # Example usage
    
    # Example 1: Comfort Seeker
    print("EXAMPLE 1: Comfort Seeker")
    print("=" * 80)
    user1 = UserTasteVector(
        spice_intensity=0.2,
        texture_intensity=0.5,
        preparation_familiarity=0.2,
        richness=0.8,
        psychological_distance=0.2
    )
    assignment1 = assign_to_rings(
        user_vector=user1,
        dislikes=set(),
        archetypes={Archetype.COMFORT_MAXIMALIST}
    )
    print(explain_ring_assignment(assignment1))
    print("\n")
    
    # Example 2: Adventurous Eater
    print("EXAMPLE 2: Adventurous Eater")
    print("=" * 80)
    user2 = UserTasteVector(
        spice_intensity=0.8,
        texture_intensity=0.8,
        preparation_familiarity=0.8,
        richness=0.5,
        psychological_distance=0.8
    )
    assignment2 = assign_to_rings(
        user_vector=user2,
        dislikes={"Cheeseburger"},
        archetypes={Archetype.FLAVOR_EXPLORER, Archetype.HEAT_SEEKER}
    )
    print(explain_ring_assignment(assignment2))
    print("\n")
    
    # Detailed food explanation
    print("DETAILED FOOD EXPLANATION:")
    print(explain_food_distance("Steak tartare", assignment2))
