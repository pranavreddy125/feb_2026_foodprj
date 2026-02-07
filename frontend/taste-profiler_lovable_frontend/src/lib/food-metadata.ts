// Food metadata with descriptions, origins, and image URLs

export interface FoodMetadata {
  name: string;
  description: string;
  origin: string;
  region: string;
  imageUrl: string;
}

export const FOOD_METADATA: Record<string, FoodMetadata> = {
  'Pizza': {
    name: 'Pizza',
    description: 'A beloved Italian creation featuring a yeasted flatbread topped with tomato sauce, cheese, and various toppings. Originally a peasant food from Naples, it became a global phenomenon after Italian immigrants brought it to America.',
    origin: 'Italy',
    region: 'Naples, Campania',
    imageUrl: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800&h=600&fit=crop&q=80',
  },
  'Sushi': {
    name: 'Sushi',
    description: 'A Japanese art form combining vinegared rice with fresh seafood, vegetables, and seaweed. Originating as a preservation method in Southeast Asia, it evolved in Japan over centuries into the refined cuisine enjoyed worldwide today.',
    origin: 'Japan',
    region: 'Tokyo & Osaka',
    imageUrl: 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800&h=600&fit=crop&q=80',
  },
  'Tacos': {
    name: 'Tacos',
    description: 'A traditional Mexican dish consisting of a corn or wheat tortilla folded around a savory filling. Dating back to pre-Columbian times, tacos represent the heart of Mexican street food culture and regional culinary traditions.',
    origin: 'Mexico',
    region: 'Central Mexico',
    imageUrl: 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=800&h=600&fit=crop&q=80',
  },
  'Pad Thai': {
    name: 'Pad Thai',
    description: 'Thailand\'s iconic stir-fried rice noodle dish with eggs, tofu, shrimp, and a perfect balance of sweet, sour, and savory flavors. Created in the 1930s as part of a Thai nation-building campaign to promote a unified cuisine.',
    origin: 'Thailand',
    region: 'Central Thailand',
    imageUrl: 'https://images.unsplash.com/photo-1559314809-0d155014e29e?w=800&h=600&fit=crop&q=80',
  },
  'Butter Chicken': {
    name: 'Butter Chicken',
    description: 'A rich, creamy tomato-based curry with tender chicken pieces marinated in yogurt and spices. Invented in Delhi in the 1950s at Moti Mahal restaurant, it has become one of the most popular Indian dishes worldwide.',
    origin: 'India',
    region: 'Delhi, North India',
    imageUrl: 'https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=800&h=600&fit=crop&q=80',
  },
  'Pho': {
    name: 'Pho',
    description: 'Vietnam\'s beloved noodle soup featuring a fragrant beef or chicken broth, rice noodles, and fresh herbs. Developed in the early 20th century in northern Vietnam, it has become the country\'s most iconic culinary export.',
    origin: 'Vietnam',
    region: 'Hanoi, Northern Vietnam',
    imageUrl: 'https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=800&h=600&fit=crop&q=80',
  },
  'Ramen': {
    name: 'Ramen',
    description: 'Japanese wheat noodles served in a rich, flavorful broth with various toppings like chashu pork and soft-boiled eggs. Though Chinese in origin, ramen was transformed into a distinctly Japanese comfort food beloved worldwide.',
    origin: 'Japan',
    region: 'Fukuoka, Sapporo, Tokyo',
    imageUrl: 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=800&h=600&fit=crop&q=80',
  },
  'Falafel': {
    name: 'Falafel',
    description: 'Deep-fried balls made from ground chickpeas or fava beans, seasoned with herbs and aromatic spices. A staple of Middle Eastern cuisine with roots tracing back to ancient Egypt, now enjoyed in pitas and wraps globally.',
    origin: 'Middle East',
    region: 'Egypt / Levant',
    imageUrl: 'https://images.unsplash.com/photo-1547058881-aa0edd92aab3?w=800&h=600&fit=crop&q=80',
  },
  'Gyros': {
    name: 'Gyros',
    description: 'Greek street food featuring meat cooked on a vertical rotisserie, served in warm pita with tomatoes, onions, and creamy tzatziki sauce. A modern classic of Greek cuisine that has found fans across Europe and beyond.',
    origin: 'Greece',
    region: 'Athens, Greece',
    imageUrl: 'https://images.unsplash.com/photo-1621852004158-f3bc188ace2d?w=800&h=600&fit=crop&q=80',
  },
  'Bibimbap': {
    name: 'Bibimbap',
    description: 'A colorful Korean rice bowl topped with sautéed vegetables, gochujang chili paste, and often a fried egg. The name means "mixed rice," reflecting its communal nature and the harmony of diverse ingredients in one dish.',
    origin: 'South Korea',
    region: 'Jeonju, Korea',
    imageUrl: 'https://images.unsplash.com/photo-1553163147-622ab57be1c7?w=800&h=600&fit=crop&q=80',
  },
  'Ceviche': {
    name: 'Ceviche',
    description: 'Fresh raw fish cured in citrus juices with onions, cilantro, and chili peppers. A coastal tradition spanning Latin America and particularly beloved in Peru, where it is considered the national dish and cultural treasure.',
    origin: 'Peru',
    region: 'Lima, Coastal Peru',
    imageUrl: 'https://images.unsplash.com/photo-1535399831218-d5bd36d1a6b3?w=800&h=600&fit=crop&q=80',
  },
  'Shakshuka': {
    name: 'Shakshuka',
    description: 'Eggs poached in a spiced tomato and pepper sauce, often served with crusty bread for dipping. Popular across North Africa and the Middle East, it has become a beloved brunch dish in cafes around the world.',
    origin: 'North Africa',
    region: 'Tunisia / Israel',
    imageUrl: 'https://images.unsplash.com/photo-1590412200988-a436970781fa?w=800&h=600&fit=crop&q=80',
  },
  'Dim Sum': {
    name: 'Dim Sum',
    description: 'A Cantonese tradition of small dishes served alongside tea, featuring dumplings, buns, and savory delicacies. Originating from teahouses along the ancient Silk Road, dim sum remains a cherished social dining experience.',
    origin: 'China',
    region: 'Guangdong, Southern China',
    imageUrl: 'https://images.unsplash.com/photo-1563245372-f21724e3856d?w=800&h=600&fit=crop&q=80',
  },
  'Paella': {
    name: 'Paella',
    description: 'Spain\'s iconic rice dish cooked in a wide, shallow pan with saffron, vegetables, and meat or seafood. Born in Valencia as a humble farmers\' meal, it evolved into a symbol of Spanish culinary heritage and celebration.',
    origin: 'Spain',
    region: 'Valencia, Spain',
    imageUrl: 'https://images.unsplash.com/photo-1534080564583-6be75777b70a?w=800&h=600&fit=crop&q=80',
  },
  'Goulash': {
    name: 'Goulash',
    description: 'A hearty Hungarian stew of tender meat, vegetables, and generous amounts of paprika. Originally a shepherds\' dish cooked over open fires on the plains, it became a proud symbol of Hungarian national identity.',
    origin: 'Hungary',
    region: 'Hungarian Plains',
    imageUrl: 'https://images.unsplash.com/photo-1504973960431-1c467e159aa4?w=800&h=600&fit=crop&q=80',
  },
  'Jerk Chicken': {
    name: 'Jerk Chicken',
    description: 'Jamaican chicken marinated in a fiery blend of allspice, scotch bonnet peppers, thyme, and aromatic herbs. A technique with roots in the Maroon people\'s traditions, representing Jamaica\'s bold and vibrant flavors.',
    origin: 'Jamaica',
    region: 'Portland, Jamaica',
    imageUrl: 'https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=800&h=600&fit=crop&q=80',
  },
  'Tom Yum': {
    name: 'Tom Yum',
    description: 'Thailand\'s famous hot and sour soup with shrimp, mushrooms, lemongrass, and aromatic herbs. A perfect balance of spicy, sour, salty, and sweet flavors that exemplifies the complexity of Thai cuisine.',
    origin: 'Thailand',
    region: 'Central Thailand',
    imageUrl: 'https://images.unsplash.com/photo-1548943487-a2e4e43b4853?w=800&h=600&fit=crop&q=80',
  },
  'Moussaka': {
    name: 'Moussaka',
    description: 'A layered casserole of eggplant, spiced meat, and creamy béchamel sauce baked to golden perfection. A cornerstone of Greek cuisine with variations found throughout the Eastern Mediterranean and Middle East.',
    origin: 'Greece',
    region: 'Greece & Eastern Mediterranean',
    imageUrl: 'https://images.unsplash.com/photo-1574484284002-952d92456975?w=800&h=600&fit=crop&q=80',
  },
};

export function getFoodMetadata(foodName: string): FoodMetadata | null {
  if (FOOD_METADATA[foodName]) {
    return FOOD_METADATA[foodName];
  }

  // Fallback for backend foods without curated metadata yet.
  return {
    name: foodName,
    description: 'A notable dish in your comfort rings with unique flavor and cultural roots.',
    origin: 'Various',
    region: 'Global',
    imageUrl: '/placeholder.svg',
  };
}
