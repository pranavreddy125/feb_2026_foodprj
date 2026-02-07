import { FoodPersonalityInput, PersonalityResult } from './food-data';

// Backend contract: POST /assign_to_rings with taste vector + optional lists.
const API_BASE_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';
const ASSIGN_RINGS_PATH = '/assign_to_rings';

type BackendFoodDistance = {
  food_name: string;
  distance: number;
  ring: number;
  dimension_contributions: Record<string, number>;
};

type BackendPersonality = {
  primary_personality: string;
  secondary_personality: string;
  confidence_primary: number;
  confidence_secondary: number;
  explanation: string;
};

type BackendRingAssignment = {
  ring_0: BackendFoodDistance[];
  ring_1: BackendFoodDistance[];
  ring_2: BackendFoodDistance[];
  personality: BackendPersonality;
};

export async function computeFoodPersonality(input: FoodPersonalityInput): Promise<PersonalityResult> {
  const payload = {
    ...input.tasteDimensions,
    dislikes: input.dislikes ?? [],
    archetypes: input.archetypes ?? [],
  };

  const response = await fetch(`${API_BASE_URL}${ASSIGN_RINGS_PATH}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    let message = `Request failed (${response.status})`;
    try {
      const errorBody = await response.json();
      if (errorBody?.message) {
        message = errorBody.message;
      }
    } catch {
      // Keep default message if the response isn't JSON.
    }
    throw new Error(message);
  }

  const data = (await response.json()) as BackendRingAssignment;

  const mapFood = (food: BackendFoodDistance) => ({
    name: food.food_name,
    distance: food.distance,
    contributions: food.dimension_contributions,
  });

  return {
    primaryPersonality: data.personality.primary_personality,
    primaryConfidence: data.personality.confidence_primary,
    secondaryPersonality: data.personality.secondary_personality || undefined,
    secondaryConfidence: data.personality.confidence_secondary ?? undefined,
    explanation: data.personality.explanation,
    comfortRings: {
      ring0: data.ring_0.map(mapFood),
      ring1: data.ring_1.map(mapFood),
      ring2: data.ring_2.map(mapFood),
    },
  };
}
