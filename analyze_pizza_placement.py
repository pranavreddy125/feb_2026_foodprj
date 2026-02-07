#!/usr/bin/env python3
"""
Diagnostic: Analyze why "Pepperoni pizza" lands in Ring 2 for adventurous user.

User vector (from description):
- high spice tolerance (0.8)
- mixed texture (0.5)
- flexible preparation familiarity (0.5)
- balanced richness (0.5)
- high curiosity (0.8)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend import UserTasteVector, assign_to_rings, FOODS
import math

# User vector matching the reported scenario
user = UserTasteVector(
    spice_intensity=0.8,
    texture_intensity=0.5,
    preparation_familiarity=0.5,
    richness=0.5,
    psychological_distance=0.8
)

# Compute assignment
assignment = assign_to_rings(user_vector=user, dislikes=set(), archetypes=set())

# Find pizza
pizza_food = None
for fd in assignment.ring_0 + assignment.ring_1 + assignment.ring_2:
    if "pizza" in fd.food_name.lower():
        pizza_food = fd
        break

print("=" * 80)
print("PIZZA PLACEMENT ANALYSIS")
print("=" * 80)
print()

print("USER VECTOR:")
print(f"  spice_intensity: {user.spice_intensity}")
print(f"  texture_intensity: {user.texture_intensity}")
print(f"  preparation_familiarity: {user.preparation_familiarity}")
print(f"  richness: {user.richness}")
print(f"  psychological_distance: {user.psychological_distance}")
print()

print("RING THRESHOLDS:")
print(f"  threshold_0 (Ring 0 max): {assignment.ring_thresholds[0]:.4f}")
print(f"  threshold_1 (Ring 1 max): {assignment.ring_thresholds[1]:.4f}")
print()

if pizza_food:
    print(f"PEPPERONI PIZZA ASSIGNMENT:")
    print(f"  Ring: {pizza_food.ring}")
    print(f"  Distance: {pizza_food.distance:.4f}")
    print()
    
    # Show pizza's food vector
    pizza_vec = FOODS["Pepperoni pizza"]
    print(f"PIZZA FOOD VECTOR: {pizza_vec}")
    print(f"  spice_intensity: {pizza_vec[0]}")
    print(f"  texture_intensity: {pizza_vec[1]}")
    print(f"  preparation_familiarity: {pizza_vec[2]}")
    print(f"  richness: {pizza_vec[3]}")
    print(f"  psychological_distance: {pizza_vec[4]}")
    print()
    
    # Compute raw dimension mismatches
    user_vec = user.to_tuple()
    print("DIMENSION-BY-DIMENSION MISMATCH:")
    dim_names = ["spice", "texture", "prep", "richness", "psych_dist"]
    total_squared_diff = 0
    for i, name in enumerate(dim_names):
        diff = user_vec[i] - pizza_vec[i]
        sq_diff = diff ** 2
        total_squared_diff += sq_diff
        print(f"  {name:15s}: user={user_vec[i]:.1f}, food={pizza_vec[i]:.1f}, diff={diff:+.1f}, sq_diff={sq_diff:.4f}")
    
    raw_distance = math.sqrt(total_squared_diff)
    print(f"\nRAW EUCLIDEAN DISTANCE: {raw_distance:.4f}")
    print(f"ACTUAL DISTANCE (with archetypes): {pizza_food.distance:.4f}")
    print()
    
    print("DIMENSION CONTRIBUTIONS:")
    for key, val in sorted(pizza_food.dimension_contributions.items()):
        print(f"  {key:30s}: {val:.4f}")
    print()

# Show all ring assignments sorted by distance
print("ALL FOOD ASSIGNMENTS (sorted by distance):")
all_foods = sorted(assignment.ring_0 + assignment.ring_1 + assignment.ring_2, key=lambda x: x.distance)
for fd in all_foods:
    ring_label = f"Ring {fd.ring}"
    marker = "  <-- PIZZA" if "pizza" in fd.food_name.lower() else ""
    print(f"  {fd.food_name:30s} {ring_label:8s} d={fd.distance:.4f}{marker}")

print()
print("=" * 80)
print("ROOT CAUSE ANALYSIS:")
print("=" * 80)
print()

# Analyze why pizza has high distance
if pizza_food:
    user_vec = user.to_tuple()
    pizza_vec = FOODS["Pepperoni pizza"]
    
    print("Pizza is encoded as:")
    print(f"  - LOW spice (0.2) vs user HIGH spice (0.8) → mismatch = 0.6")
    print(f"  - MID texture (0.5) vs user MID texture (0.5) → match = 0.0")
    print(f"  - LOW prep familiarity (0.2) vs user MID prep (0.5) → mismatch = 0.3")
    print(f"  - HIGH richness (0.8) vs user MID richness (0.5) → mismatch = 0.3")
    print(f"  - LOW psych distance (0.2) vs user HIGH psych distance (0.8) → mismatch = 0.6")
    print()
    print("PRIMARY ISSUE: Pizza is coded as a LOW-adventure food (psych_dist=0.2)")
    print("               But user has HIGH adventure tolerance (psych_dist=0.8)")
    print("               This creates a large penalty (0.6^2 = 0.36) in just one dimension.")
    print()
    print("SECONDARY ISSUE: Pizza is coded as LOW spice (0.2)")
    print("                 User seeks HIGH spice (0.8)")
    print("                 This creates another large penalty (0.6^2 = 0.36)")
    print()
    print("Combined: These two mismatches contribute 0.72 to squared distance")
    print(f"         √(0.72 + other dims) = {pizza_food.distance:.4f}")
    print()

# Count ring distribution
print("RING DISTRIBUTION:")
print(f"  Ring 0 (Core Comfort): {len(assignment.ring_0)} foods")
print(f"  Ring 1 (Safe Stretch): {len(assignment.ring_1)} foods")
print(f"  Ring 2 (Experimental): {len(assignment.ring_2)} foods")
print()

# Show culturally familiar foods and their rings
print("CULTURALLY FAMILIAR 'ANCHOR' FOODS:")
anchor_foods = ["Cheeseburger", "Pepperoni pizza", "Fried chicken", "Pasta with red sauce"]
for name in anchor_foods:
    for fd in all_foods:
        if fd.food_name == name:
            print(f"  {name:25s} → Ring {fd.ring} (d={fd.distance:.4f})")
            break
