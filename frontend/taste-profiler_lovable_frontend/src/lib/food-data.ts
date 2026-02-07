// Fixed data for the Food Personality system

export const TASTE_DIMENSIONS = [
  { 
    id: 'spice_intensity', 
    label: 'Spice Intensity',
    description: 'How much heat do you enjoy?',
    options: [
      { value: 0.2, label: 'Mild', description: 'Little to no spice' },
      { value: 0.5, label: 'Medium', description: 'Moderate heat' },
      { value: 0.8, label: 'Hot', description: 'Bring on the fire' },
    ]
  },
  { 
    id: 'texture_intensity', 
    label: 'Texture Intensity',
    description: 'Your preference for textural complexity',
    options: [
      { value: 0.2, label: 'Smooth', description: 'Soft, uniform textures' },
      { value: 0.5, label: 'Mixed', description: 'Some variety is nice' },
      { value: 0.8, label: 'Complex', description: 'Love crunchy, chewy, varied' },
    ]
  },
  { 
    id: 'preparation_familiarity', 
    label: 'Preparation Familiarity',
    description: 'How adventurous with cooking methods?',
    options: [
      { value: 0.2, label: 'Traditional', description: 'Classic, familiar methods' },
      { value: 0.5, label: 'Flexible', description: 'Open to some variation' },
      { value: 0.8, label: 'Adventurous', description: 'Love novel techniques' },
    ]
  },
  { 
    id: 'richness', 
    label: 'Richness',
    description: 'Your preference for rich, indulgent foods',
    options: [
      { value: 0.2, label: 'Light', description: 'Fresh, clean flavors' },
      { value: 0.5, label: 'Balanced', description: 'Moderate richness' },
      { value: 0.8, label: 'Indulgent', description: 'Rich, decadent foods' },
    ]
  },
  { 
    id: 'psychological_distance', 
    label: 'Psychological Distance',
    description: 'Comfort with unfamiliar cuisines',
    options: [
      { value: 0.2, label: 'Familiar', description: 'Stick to what I know' },
      { value: 0.5, label: 'Curious', description: 'Occasionally try new things' },
      { value: 0.8, label: 'Explorer', description: 'Always seeking the unknown' },
    ]
  },
] as const;

export const FOODS = [
  'Cheeseburger',
  'Pepperoni pizza',
  'Fried chicken',
  'Butter chicken',
  'Pasta with red sauce',
  'Tacos al pastor',
  'Ethiopian injera with stew',
  'Sushi',
  'Pho',
  'Falafel wrap',
  'Beef tongue tacos',
  'Lamb curry',
  'Kimchi stew',
  'Oxtail stew',
  'Steak tartare',
  'Escargot',
  'Haggis',
  'Fufu',
] as const;

export const ARCHETYPES = [
  {
    id: 'texture_avoider',
    label: 'Texture Avoider',
    description: 'Prefers smoother, more uniform textures',
  },
  {
    id: 'heat_seeker',
    label: 'Heat Seeker',
    description: 'Enjoys spicy foods and bold heat',
  },
  {
    id: 'comfort_maximalist',
    label: 'Comfort Maximalist',
    description: 'Leans strongly toward familiar comfort foods',
  },
  {
    id: 'flavor_explorer',
    label: 'Flavor Explorer',
    description: 'Seeks variety and adventurous flavors',
  },
  {
    id: 'refined_minimalist',
    label: 'Refined Minimalist',
    description: 'Prefers lighter, simpler, refined dishes',
  },
] as const;

export type TasteDimensionId = typeof TASTE_DIMENSIONS[number]['id'];
export type Food = typeof FOODS[number];
export type ArchetypeId = typeof ARCHETYPES[number]['id'];

export interface TasteDimensions {
  spice_intensity: number;
  texture_intensity: number;
  preparation_familiarity: number;
  richness: number;
  psychological_distance: number;
}

export interface FoodPersonalityInput {
  tasteDimensions: TasteDimensions;
  dislikes: Food[];
  archetypes: ArchetypeId[];
}

export interface ComfortFood {
  name: string;
  distance: number;
  contributions?: Record<string, number>;
}

export interface ComfortRings {
  ring0: ComfortFood[]; // Core Comfort
  ring1: ComfortFood[]; // Safe Stretch
  ring2: ComfortFood[]; // Experimental
}

export interface PersonalityResult {
  primaryPersonality: string;
  primaryConfidence: number;
  secondaryPersonality?: string;
  secondaryConfidence?: number;
  explanation: string;
  comfortRings: ComfortRings;
}
