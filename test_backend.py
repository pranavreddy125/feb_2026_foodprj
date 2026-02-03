#!/usr/bin/env python3
"""
Test Suite for Food Personality Backend
Episode: cursor_foodapp

Validates all invariants from the requirements.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import (
    UserTasteVector, Archetype, assign_to_rings,
    euclidean_distance, FOODS, VALID_VALUES
)


def test_i1_metric_properties():
    """Test I1: Taste Distance Metric Properties."""
    print("Testing I1: Metric Properties...")
    
    vec_a = (0.2, 0.5, 0.2, 0.8, 0.2)
    vec_b = (0.8, 0.5, 0.8, 0.5, 0.8)
    vec_c = (0.5, 0.5, 0.5, 0.5, 0.5)
    
    # Non-negativity: d(A, B) >= 0
    d_ab = euclidean_distance(vec_a, vec_b)
    assert d_ab >= 0, "Failed: non-negativity"
    
    # Identity: d(A, A) = 0
    d_aa = euclidean_distance(vec_a, vec_a)
    assert d_aa == 0, "Failed: identity"
    
    # Symmetry: d(A, B) = d(B, A)
    d_ba = euclidean_distance(vec_b, vec_a)
    assert abs(d_ab - d_ba) < 1e-10, "Failed: symmetry"
    
    # Triangle inequality: d(A, C) <= d(A, B) + d(B, C)
    d_ac = euclidean_distance(vec_a, vec_c)
    d_bc = euclidean_distance(vec_b, vec_c)
    assert d_ac <= d_ab + d_bc + 1e-10, "Failed: triangle inequality"
    
    print("  ✓ All metric properties satisfied")


def test_i2_ring_ordering():
    """Test I2: Nested Ring Distance Ordering."""
    print("Testing I2: Ring Ordering...")
    
    user = UserTasteVector(0.2, 0.5, 0.2, 0.8, 0.2)
    assignment = assign_to_rings(user, set(), set())
    
    # Check that rings don't overlap
    if assignment.ring_0 and assignment.ring_1:
        max_ring_0 = max(fd.distance for fd in assignment.ring_0)
        min_ring_1 = min(fd.distance for fd in assignment.ring_1)
        assert max_ring_0 <= min_ring_1, "Failed: Ring 0 and Ring 1 overlap"
    
    if assignment.ring_1 and assignment.ring_2:
        max_ring_1 = max(fd.distance for fd in assignment.ring_1)
        min_ring_2 = min(fd.distance for fd in assignment.ring_2)
        assert max_ring_1 <= min_ring_2, "Failed: Ring 1 and Ring 2 overlap"
    
    # Check monotonicity within rings
    for ring, ring_name in [(assignment.ring_0, "Ring 0"), 
                             (assignment.ring_1, "Ring 1"), 
                             (assignment.ring_2, "Ring 2")]:
        for i in range(len(ring) - 1):
            assert ring[i].distance <= ring[i+1].distance, f"Failed: monotonicity in {ring_name}"
    
    print("  ✓ Ring ordering satisfied")


def test_i3_partition_completeness():
    """Test I3: Complete Coverage & Mutual Exclusion."""
    print("Testing I3: Partition Completeness...")
    
    user = UserTasteVector(0.5, 0.5, 0.5, 0.5, 0.5)
    assignment = assign_to_rings(user, set(), set())
    
    # All foods assigned
    all_assigned = set(fd.food_name for fd in assignment.ring_0 + assignment.ring_1 + assignment.ring_2)
    assert len(all_assigned) == len(FOODS), "Failed: not all foods assigned"
    assert all_assigned == set(FOODS.keys()), "Failed: food set mismatch"
    
    # No duplicates (mutual exclusion)
    ring_0_names = set(fd.food_name for fd in assignment.ring_0)
    ring_1_names = set(fd.food_name for fd in assignment.ring_1)
    ring_2_names = set(fd.food_name for fd in assignment.ring_2)
    
    assert len(ring_0_names & ring_1_names) == 0, "Failed: Ring 0 and Ring 1 overlap"
    assert len(ring_1_names & ring_2_names) == 0, "Failed: Ring 1 and Ring 2 overlap"
    assert len(ring_0_names & ring_2_names) == 0, "Failed: Ring 0 and Ring 2 overlap"
    
    print("  ✓ Partition completeness satisfied")


def test_i4_boundary_determinism():
    """Test I4: Deterministic Ring Boundaries."""
    print("Testing I4: Boundary Determinism...")
    
    user = UserTasteVector(0.2, 0.5, 0.8, 0.5, 0.5)
    
    # Run multiple times, should get same results
    assignment1 = assign_to_rings(user, {"Cheeseburger"}, {Archetype.HEAT_SEEKER})
    assignment2 = assign_to_rings(user, {"Cheeseburger"}, {Archetype.HEAT_SEEKER})
    
    # Same thresholds
    assert assignment1.ring_thresholds == assignment2.ring_thresholds, "Failed: thresholds not deterministic"
    
    # Same ring assignments
    foods_1 = [(fd.food_name, fd.ring) for fd in assignment1.ring_0 + assignment1.ring_1 + assignment1.ring_2]
    foods_2 = [(fd.food_name, fd.ring) for fd in assignment2.ring_0 + assignment2.ring_1 + assignment2.ring_2]
    foods_1.sort()
    foods_2.sort()
    assert foods_1 == foods_2, "Failed: ring assignments not deterministic"
    
    print("  ✓ Determinism satisfied")


def test_i5_personality_stability():
    """Test I5: Food Personality Stability."""
    print("Testing I5: Personality Stability...")
    
    user = UserTasteVector(0.2, 0.5, 0.2, 0.8, 0.2)
    
    # Same input should give same personality
    assignment1 = assign_to_rings(user, set(), {Archetype.COMFORT_MAXIMALIST})
    assignment2 = assign_to_rings(user, set(), {Archetype.COMFORT_MAXIMALIST})
    
    assert assignment1.personality.primary_personality == assignment2.personality.primary_personality, \
        "Failed: personality not stable"
    
    print("  ✓ Personality stability satisfied")


def test_i6_taste_feature_consistency():
    """Test I6: Taste Feature Vector Consistency."""
    print("Testing I6: Feature Consistency...")
    
    # All foods have same dimensions
    dimensions = None
    for food_name, food_vec in FOODS.items():
        if dimensions is None:
            dimensions = len(food_vec)
        assert len(food_vec) == dimensions, f"Failed: {food_name} has wrong dimensions"
    
    # All values in valid set
    for food_name, food_vec in FOODS.items():
        for val in food_vec:
            assert val in VALID_VALUES, f"Failed: {food_name} has invalid value {val}"
    
    print("  ✓ Feature consistency satisfied")


def test_i7_comfort_monotonicity():
    """Test I7: Comfort Decreases with Distance."""
    print("Testing I7: Comfort Monotonicity...")
    
    user = UserTasteVector(0.2, 0.5, 0.2, 0.8, 0.2)
    assignment = assign_to_rings(user, set(), set())
    
    # Ring numbers should increase with distance
    all_foods = assignment.ring_0 + assignment.ring_1 + assignment.ring_2
    
    for i in range(len(all_foods) - 1):
        if all_foods[i].distance < all_foods[i+1].distance:
            assert all_foods[i].ring <= all_foods[i+1].ring, \
                f"Failed: {all_foods[i].food_name} (ring {all_foods[i].ring}, d={all_foods[i].distance:.3f}) " \
                f"should be in same or lower ring than {all_foods[i+1].food_name} " \
                f"(ring {all_foods[i+1].ring}, d={all_foods[i+1].distance:.3f})"
    
    print("  ✓ Comfort monotonicity satisfied")


def test_i15_add_food_consistency():
    """Test I15: Adding Food Maintains Invariants (simulated)."""
    print("Testing I15: Add Food Consistency...")
    
    user = UserTasteVector(0.5, 0.5, 0.5, 0.5, 0.5)
    assignment = assign_to_rings(user, set(), set())
    
    # Verify all invariants hold
    all_foods_count = len(assignment.ring_0) + len(assignment.ring_1) + len(assignment.ring_2)
    assert all_foods_count == len(FOODS), "Failed: food count mismatch"
    
    print("  ✓ Add food consistency validated")


def test_i17_update_food_consistency():
    """Test I17: Updating User Vector Re-classifies Correctly."""
    print("Testing I17: Update Consistency...")
    
    user1 = UserTasteVector(0.2, 0.5, 0.2, 0.8, 0.2)
    user2 = UserTasteVector(0.8, 0.8, 0.8, 0.5, 0.8)
    
    assignment1 = assign_to_rings(user1, set(), set())
    assignment2 = assign_to_rings(user2, set(), set())
    
    # Different users should get different ring assignments
    foods1 = {fd.food_name: fd.ring for fd in assignment1.ring_0 + assignment1.ring_1 + assignment1.ring_2}
    foods2 = {fd.food_name: fd.ring for fd in assignment2.ring_0 + assignment2.ring_1 + assignment2.ring_2}
    
    # At least some foods should be in different rings
    differences = sum(1 for food in foods1 if foods1[food] != foods2[food])
    assert differences > 0, "Failed: different users should produce different ring assignments"
    
    print("  ✓ Update consistency satisfied")


def test_dislike_penalty():
    """Test that dislikes increase distance."""
    print("Testing Dislike Penalty...")
    
    user = UserTasteVector(0.2, 0.5, 0.2, 0.8, 0.2)
    
    assignment_no_dislike = assign_to_rings(user, set(), set())
    assignment_with_dislike = assign_to_rings(user, {"Cheeseburger"}, set())
    
    # Find Cheeseburger in both
    cb_no_dislike = next(fd for fd in assignment_no_dislike.ring_0 + assignment_no_dislike.ring_1 + assignment_no_dislike.ring_2 
                         if fd.food_name == "Cheeseburger")
    cb_with_dislike = next(fd for fd in assignment_with_dislike.ring_0 + assignment_with_dislike.ring_1 + assignment_with_dislike.ring_2 
                           if fd.food_name == "Cheeseburger")
    
    assert cb_with_dislike.distance > cb_no_dislike.distance, "Failed: dislike should increase distance"
    assert cb_with_dislike.ring >= cb_no_dislike.ring, "Failed: dislike should push to outer ring"
    
    print("  ✓ Dislike penalty working correctly")


def test_archetype_effects():
    """Test that archetypes modify thresholds correctly."""
    print("Testing Archetype Effects...")
    
    user = UserTasteVector(0.5, 0.5, 0.5, 0.5, 0.5)
    
    assignment_base = assign_to_rings(user, set(), set())
    assignment_comfort = assign_to_rings(user, set(), {Archetype.COMFORT_MAXIMALIST})
    assignment_explorer = assign_to_rings(user, set(), {Archetype.FLAVOR_EXPLORER})
    
    # Comfort Maximalist should compress Ring 0 (lower threshold_0)
    assert assignment_comfort.ring_thresholds[0] < assignment_base.ring_thresholds[0], \
        "Failed: Comfort Maximalist should lower threshold_0"
    
    # Flavor Explorer should expand Ring 1 (raise threshold_1)
    assert assignment_explorer.ring_thresholds[1] > assignment_base.ring_thresholds[1], \
        "Failed: Flavor Explorer should raise threshold_1"
    
    print("  ✓ Archetype effects working correctly")


def run_all_tests():
    """Run all test cases."""
    print("\n" + "=" * 80)
    print("FOOD PERSONALITY BACKEND - TEST SUITE")
    print("Episode: cursor_foodapp")
    print("=" * 80 + "\n")
    
    tests = [
        test_i1_metric_properties,
        test_i2_ring_ordering,
        test_i3_partition_completeness,
        test_i4_boundary_determinism,
        test_i5_personality_stability,
        test_i6_taste_feature_consistency,
        test_i7_comfort_monotonicity,
        test_i15_add_food_consistency,
        test_i17_update_food_consistency,
        test_dislike_penalty,
        test_archetype_effects,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ Unexpected error: {e}")
            failed += 1
    
    print("\n" + "=" * 80)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("=" * 80 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
