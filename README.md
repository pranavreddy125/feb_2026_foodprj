# Food Personality Backend

Clean, modular backend for a 3-ring comfort food assignment system.

## Quick Start

```bash
# Run examples
cd 2_2026_cursor_foodprj
python backend/main.py

# Run tests
python test_backend.py
```

## System Overview

- **3 Comfort Rings**: Ring 0 (Core), Ring 1 (Safe Stretch), Ring 2 (Experimental)
- **18 Fixed Foods**: From Cheeseburger to Fufu  
- **5 Semantic Dimensions**: spice, texture, prep familiarity, richness, psych distance
- **5 Archetypes**: Modify ring thresholds based on user preferences
- **Deterministic**: No ML, no embeddings, no external APIs

## Project Structure

```
2_2026_cursor_foodprj/
├── backend/
│   ├── __init__.py           # Package exports
│   ├── food_data.py          # 18 foods with semantic profiles
│   ├── taste_vector.py       # Data structures
│   ├── archetypes.py         # User archetypes enum
│   ├── distance.py           # Distance calculation
│   ├── ring_assignment.py    # Ring assignment logic
│   ├── explanations.py       # Personality & explanations
│   └── main.py               # Example usage
├── test_backend.py           # Test suite (11 tests)
├── README.md                 # This file
└── requirements.txt          # Dependencies
```

## Usage Example

```python
from backend import UserTasteVector, Archetype, assign_to_rings

# Define user taste preferences
user = UserTasteVector(
    spice_intensity=0.2,
    texture_intensity=0.5,
    preparation_familiarity=0.2,
    richness=0.8,
    psychological_distance=0.2
)

# Assign foods to rings
assignment = assign_to_rings(
    user_vector=user,
    dislikes=set(),
    archetypes={Archetype.COMFORT_MAXIMALIST}
)

# Results include:
# - assignment.ring_0, ring_1, ring_2 (food lists)
# - assignment.personality (primary + secondary)
# - assignment.ring_thresholds
```

## Test Results

```
11 tests passed, 0 failed
✓ I1: Metric Properties
✓ I2: Ring Ordering
✓ I3: Partition Completeness
✓ I4: Determinism
✓ I5: Personality Stability
✓ I6: Feature Consistency
✓ I7: Comfort Monotonicity
✓ I15: Add Food Consistency
✓ I17: Update Consistency
✓ Dislike Penalty
✓ Archetype Effects
```

## Episode

Part of A1 episode `cursor_foodapp` with full temporal tracking.
