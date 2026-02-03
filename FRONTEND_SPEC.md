# Frontend Specification - Food Personality System

**Backend Version**: 1.0.0  
**Episode**: cursor_foodapp  
**Date**: 2026-01-31

This document defines the complete contract between backend and frontend. All data structures, types, and interactions are derived from the existing backend implementation.

---

## 1. INPUT DATA (User-Provided)

### 1.1 User Taste Vector

| Field | Type | Valid Values | Source | Update Frequency | Required |
|-------|------|--------------|--------|------------------|----------|
| `spice_intensity` | number (float) | 0.2, 0.5, 0.8 | User input | User-driven | ✅ Required |
| `texture_intensity` | number (float) | 0.2, 0.5, 0.8 | User input | User-driven | ✅ Required |
| `preparation_familiarity` | number (float) | 0.2, 0.5, 0.8 | User input | User-driven | ✅ Required |
| `richness` | number (float) | 0.2, 0.5, 0.8 | User input | User-driven | ✅ Required |
| `psychological_distance` | number (float) | 0.2, 0.5, 0.8 | User input | User-driven | ✅ Required |

**Validation**: All values must be exactly 0.2, 0.5, or 0.8. No other values accepted.

### 1.2 Dislikes

| Field | Type | Valid Values | Source | Update Frequency | Required |
|-------|------|--------------|--------|------------------|----------|
| `dislikes` | list[string] | Food names from FOODS list | User selection | User-driven | ❌ Optional (empty list if none) |

**Validation**: Each dislike must be a valid food name from the 18-food universe.

### 1.3 Archetypes

| Field | Type | Valid Values | Source | Update Frequency | Required |
|-------|------|--------------|--------|------------------|----------|
| `archetypes` | list[enum] | See Archetype enum below | User selection | User-driven | ❌ Optional (empty list if none) |

**Valid Archetype Values**:
- `"texture_avoider"`
- `"heat_seeker"`
- `"comfort_maximalist"`
- `"flavor_explorer"`
- `"refined_minimalist"`

---

## 2. STATIC REFERENCE DATA

### 2.1 Food Universe

| Field | Type | Source | Update Frequency | Required |
|-------|------|--------|------------------|----------|
| `food_name` | string | Backend FOODS constant | Static | ✅ Required |
| `semantic_profile` | tuple[5 floats] | Backend FOODS constant | Static | ✅ Required |

**Total Foods**: 18 (fixed)

**Food List**:
1. Cheeseburger
2. Pepperoni pizza
3. Fried chicken
4. Butter chicken
5. Pasta with red sauce
6. Tacos al pastor
7. Ethiopian injera with stew
8. Sushi
9. Pho
10. Falafel wrap
11. Beef tongue tacos
12. Lamb curry
13. Kimchi stew
14. Oxtail stew
15. Steak tartare
16. Escargot
17. Haggis
18. Fufu

### 2.2 Dimension Names

| Field | Type | Source | Update Frequency | Required |
|-------|------|--------|------------------|----------|
| `dimension_names` | list[string] (length 5) | Backend DIMENSION_NAMES constant | Static | ✅ Required |

**Values**:
1. `"spice_intensity"`
2. `"texture_intensity"`
3. `"preparation_familiarity"`
4. `"richness"`
5. `"psychological_distance"`

### 2.3 Valid Input Values

| Field | Type | Source | Update Frequency | Required |
|-------|------|--------|------------------|----------|
| `valid_values` | list[number] (length 3) | Backend VALID_VALUES constant | Static | ✅ Required |

**Values**: `[0.2, 0.5, 0.8]`

---

## 3. OUTPUT DATA (Backend-Computed)

### 3.1 Ring Assignment Result

**Object**: `ComfortRingAssignment`

| Field | Type | Source | Update Frequency | Required |
|-------|------|--------|------------------|----------|
| `user_vector` | UserTasteVector object | Echo of input | Computed | ✅ Required |
| `dislikes` | set[string] | Echo of input | Computed | ✅ Required |
| `archetypes` | set[Archetype enum] | Echo of input | Computed | ✅ Required |
| `ring_0` | list[FoodDistance] | Backend computation | Computed | ✅ Required |
| `ring_1` | list[FoodDistance] | Backend computation | Computed | ✅ Required |
| `ring_2` | list[FoodDistance] | Backend computation | Computed | ✅ Required |
| `personality` | PersonalityProfile object | Backend computation | Computed | ✅ Required |
| `ring_thresholds` | tuple[2 floats] | Backend computation | Computed | ✅ Required |

### 3.2 Food Distance (per food)

**Object**: `FoodDistance`

| Field | Type | Source | Update Frequency | Required |
|-------|------|--------|------------------|----------|
| `food_name` | string | Backend computation | Computed | ✅ Required |
| `distance` | number (float) | Backend computation | Computed | ✅ Required |
| `ring` | number (int) | 0, 1, or 2 | Computed | ✅ Required |
| `dimension_contributions` | object (dict) | Backend computation | Computed | ✅ Required |

**dimension_contributions structure**:
- Keys: dimension names (strings) + optional penalty/reduction keys
- Values: floats (contribution to distance)
- Example keys: `"spice_intensity"`, `"texture_intensity"`, `"dislike_penalty"`, `"heat_seeker_reduction"`

### 3.3 Personality Profile

**Object**: `PersonalityProfile`

| Field | Type | Source | Update Frequency | Required |
|-------|------|--------|------------------|----------|
| `primary_personality` | string (enum) | Backend computation | Computed | ✅ Required |
| `secondary_personality` | string (enum) | Backend computation | Computed | ✅ Required |
| `confidence_primary` | number (float 0-1) | Backend computation | Computed | ✅ Required |
| `confidence_secondary` | number (float 0-1) | Backend computation | Computed | ✅ Required |
| `explanation` | string | Backend computation | Computed | ✅ Required |

**Valid Personality Types**:
- `"Comfort Seeker"`
- `"Spice Lover"`
- `"Texture Explorer"`
- `"Adventurous Eater"`
- `"Minimalist"`
- `"Balanced Eater"`
- `"Rich Food Lover"`
- `"Familiar First"`
- `"Global Palate"`

### 3.4 Ring Thresholds

| Field | Type | Source | Update Frequency | Required |
|-------|------|--------|------------------|----------|
| `threshold_0` | number (float) | Backend computation | Computed | ✅ Required |
| `threshold_1` | number (float) | Backend computation | Computed | ✅ Required |

**Semantics**:
- `distance <= threshold_0` → Ring 0 (Core Comfort)
- `threshold_0 < distance <= threshold_1` → Ring 1 (Safe Stretch)
- `distance > threshold_1` → Ring 2 (Experimental)

---

## 4. REQUIRED INTERACTIONS

### 4.1 Primary Flow

| Interaction | Input | Output | Trigger | Required |
|-------------|-------|--------|---------|----------|
| Compute Rings | UserTasteVector + dislikes + archetypes | ComfortRingAssignment | User submits form | ✅ Required |

### 4.2 Optional Interactions

| Interaction | Input | Output | Trigger | Required |
|-------------|-------|--------|---------|----------|
| Get Food Universe | None | List of 18 foods with profiles | Page load | ❌ Optional (can be hardcoded) |
| Get Archetypes | None | List of 5 archetype IDs | Page load | ❌ Optional (can be hardcoded) |
| Get Dimension Names | None | List of 5 dimension names | Page load | ❌ Optional (can be hardcoded) |
| Get Valid Values | None | List of 3 valid values | Page load | ❌ Optional (can be hardcoded) |

---

## 5. DISPLAY REQUIREMENTS

### 5.1 Input Collection (MVP Required)

| Data to Collect | Display Type | Validation | Required |
|-----------------|--------------|------------|----------|
| Spice Intensity | Selection (0.2, 0.5, 0.8) | Must be one of 3 values | ✅ Required |
| Texture Intensity | Selection (0.2, 0.5, 0.8) | Must be one of 3 values | ✅ Required |
| Preparation Familiarity | Selection (0.2, 0.5, 0.8) | Must be one of 3 values | ✅ Required |
| Richness | Selection (0.2, 0.5, 0.8) | Must be one of 3 values | ✅ Required |
| Psychological Distance | Selection (0.2, 0.5, 0.8) | Must be one of 3 values | ✅ Required |
| Dislikes | Multi-select from 18 foods | Must be valid food names | ❌ Optional |
| Archetypes | Multi-select from 5 archetypes | Must be valid archetype IDs | ❌ Optional |

### 5.2 Results Display (MVP Required)

| Data to Display | Type | Source Field | Required |
|-----------------|------|--------------|----------|
| Ring 0 Foods | List of food names + distances | `ring_0` array | ✅ Required |
| Ring 1 Foods | List of food names + distances | `ring_1` array | ✅ Required |
| Ring 2 Foods | List of food names + distances | `ring_2` array | ✅ Required |
| Primary Personality | String | `personality.primary_personality` | ✅ Required |
| Primary Confidence | Percentage (0-100%) | `personality.confidence_primary` | ✅ Required |
| Secondary Personality | String | `personality.secondary_personality` | ❌ Optional |
| Secondary Confidence | Percentage (0-100%) | `personality.confidence_secondary` | ❌ Optional |
| Personality Explanation | Text | `personality.explanation` | ✅ Required |

### 5.3 Ring Metadata Display (MVP Optional)

| Data to Display | Type | Source Field | Required |
|-----------------|------|--------------|----------|
| Ring 0 Threshold | Number | `ring_thresholds[0]` | ❌ Optional |
| Ring 1 Threshold | Number | `ring_thresholds[1]` | ❌ Optional |
| Ring 0 Count | Number | `len(ring_0)` | ❌ Optional |
| Ring 1 Count | Number | `len(ring_1)` | ❌ Optional |
| Ring 2 Count | Number | `len(ring_2)` | ❌ Optional |

### 5.4 Food Detail Display (MVP Optional)

| Data to Display | Type | Source Field | Required |
|-----------------|------|--------------|----------|
| Food Name | String | `food_name` | ✅ Required (if showing detail) |
| Distance | Number (3 decimals) | `distance` | ✅ Required (if showing detail) |
| Ring Number | Integer (0, 1, or 2) | `ring` | ✅ Required (if showing detail) |
| Dimension Contributions | Key-value pairs | `dimension_contributions` | ❌ Optional |

---

## 6. DATA FLOW

### 6.1 Input → Backend

```
User Input:
{
  "spice_intensity": 0.2,
  "texture_intensity": 0.5,
  "preparation_familiarity": 0.2,
  "richness": 0.8,
  "psychological_distance": 0.2,
  "dislikes": ["Escargot"],
  "archetypes": ["comfort_maximalist"]
}

↓ (API call to backend)

Backend Function:
assign_to_rings(user_vector, dislikes, archetypes)
```

### 6.2 Backend → Output

```
Backend Output:
{
  "user_vector": { ... },
  "dislikes": ["Escargot"],
  "archetypes": ["comfort_maximalist"],
  "ring_0": [
    {
      "food_name": "Cheeseburger",
      "distance": 0.0,
      "ring": 0,
      "dimension_contributions": { ... }
    },
    ...
  ],
  "ring_1": [ ... ],
  "ring_2": [ ... ],
  "personality": {
    "primary_personality": "Comfort Seeker",
    "secondary_personality": "Familiar First",
    "confidence_primary": 0.3714,
    "confidence_secondary": 0.2857,
    "explanation": "Your preparation familiarity preference is 0.2 (low) | ..."
  },
  "ring_thresholds": [0.416, 0.900]
}
```

---

## 7. VALIDATION RULES

### 7.1 Input Validation (Frontend Must Enforce)

| Field | Rule | Error Message |
|-------|------|---------------|
| All taste dimensions | Must be exactly 0.2, 0.5, or 0.8 | "Value must be 0.2, 0.5, or 0.8" |
| Dislikes | Must be from 18-food list | "Invalid food name" |
| Archetypes | Must be from 5-archetype list | "Invalid archetype" |
| All taste dimensions | Cannot be null/undefined | "All dimensions required" |

### 7.2 Output Validation (Frontend Should Check)

| Field | Rule | Fallback |
|-------|------|----------|
| ring_0 + ring_1 + ring_2 | Total must equal 18 foods | Display error |
| Each food | Must appear in exactly one ring | Display error |
| Personality confidence | Must be between 0 and 1 | Clamp to range |
| Ring thresholds | threshold_0 < threshold_1 | Display error |

---

## 8. ERROR STATES

### 8.1 Input Errors (Frontend Handles)

| Error | Cause | Required Handling |
|-------|-------|-------------------|
| Invalid dimension value | User enters value not in [0.2, 0.5, 0.8] | Prevent submission, show error |
| Missing dimension | User hasn't selected all 5 dimensions | Prevent submission, show error |
| Invalid dislike | User selects non-existent food | Prevent submission, show error |
| Invalid archetype | User selects non-existent archetype | Prevent submission, show error |

### 8.2 Backend Errors (Frontend Handles)

| Error | Cause | Required Handling |
|-------|-------|-------------------|
| Validation error | Backend rejects invalid input | Display error message |
| Computation error | Backend fails to compute | Display error message |
| Network error | API call fails | Display error message, allow retry |

---

## 9. PERFORMANCE REQUIREMENTS

| Metric | Requirement | Notes |
|--------|-------------|-------|
| Computation time | < 100ms | Backend is deterministic, no ML |
| Input validation | Instant | Frontend-side validation |
| Results display | < 1 second | Including network + render |

---

## 10. DATA PERSISTENCE (Optional)

| Data | Persistence | Required |
|------|-------------|----------|
| User taste vector | Local storage / session | ❌ Optional |
| Dislikes | Local storage / session | ❌ Optional |
| Archetypes | Local storage / session | ❌ Optional |
| Last result | Local storage / session | ❌ Optional |

**Note**: Backend is stateless. All persistence is frontend responsibility.

---

## 11. FUTURE EXTENSIBILITY (Not in Current Backend)

The following are **NOT** in the current backend and should **NOT** be implemented:

- ❌ User accounts / authentication
- ❌ Saving multiple profiles
- ❌ Sharing results
- ❌ Food recommendations beyond rings
- ❌ Recipe suggestions
- ❌ Dietary restrictions
- ❌ Nutritional information
- ❌ Real-time updates
- ❌ Social features
- ❌ Machine learning
- ❌ Dynamic food list

---

## 12. MINIMUM VIABLE PRODUCT (MVP) CHECKLIST

### Must Have (Required for MVP)

- ✅ Input form for 5 taste dimensions (0.2, 0.5, 0.8 selection)
- ✅ Submit button to compute rings
- ✅ Display Ring 0 foods (Core Comfort)
- ✅ Display Ring 1 foods (Safe Stretch)
- ✅ Display Ring 2 foods (Experimental)
- ✅ Display primary personality
- ✅ Display primary confidence
- ✅ Display personality explanation
- ✅ Input validation (prevent invalid values)
- ✅ Error handling (display errors)

### Should Have (Enhances MVP)

- ⭕ Dislike selection (multi-select from 18 foods)
- ⭕ Archetype selection (multi-select from 5 archetypes)
- ⭕ Display food distances
- ⭕ Display ring counts
- ⭕ Display secondary personality

### Could Have (Nice to Have)

- ⚪ Display ring thresholds
- ⚪ Display dimension contributions per food
- ⚪ Food detail view on click
- ⚪ Save/load user preferences
- ⚪ Export results

---

**End of Specification**

This document defines the complete contract between backend and frontend based solely on the existing backend implementation. No features have been invented. All data structures, types, and interactions are directly derived from the backend code.
