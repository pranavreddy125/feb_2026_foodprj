"""
Food Registry - Single Source of Truth for Food Metadata
Episode: postvibereportmajorfixes_2026

This module consolidates all food data:
- Semantic profiles (5D taste vectors)
- Display metadata (names, descriptions, origins)
- Image URLs

All 18 foods are registered here. The API validates on startup that
every food has complete metadata.
"""

from dataclasses import dataclass
from typing import Tuple, Dict


@dataclass(frozen=True)
class FoodProfile:
    """Complete food profile with semantic and display metadata."""
    
    # Identity
    food_id: str  # Stable identifier (matches FOODS dict key)
    display_name: str  # Human-readable name
    
    # Semantic profile (5D taste vector)
    spice_intensity: float  # 0.2 (low), 0.5 (medium), 0.8 (high)
    texture_intensity: float
    preparation_familiarity: float
    richness: float
    psychological_distance: float
    
    # Display metadata
    description: str
    origin: str
    region: str
    image_url: str
    
    def to_taste_tuple(self) -> Tuple[float, float, float, float, float]:
        """Convert to tuple for backward compatibility with existing code."""
        return (
            self.spice_intensity,
            self.texture_intensity,
            self.preparation_familiarity,
            self.richness,
            self.psychological_distance
        )


# Complete Food Registry - 18 foods with full metadata
FOOD_REGISTRY: Dict[str, FoodProfile] = {
    "Cheeseburger": FoodProfile(
        food_id="Cheeseburger",
        display_name="Cheeseburger",
        spice_intensity=0.2,
        texture_intensity=0.5,
        preparation_familiarity=0.2,
        richness=0.8,
        psychological_distance=0.2,
        description="A classic American comfort food featuring a beef patty, melted cheese, and condiments on a toasted bun. The quintessential fast-food icon that has become a global symbol of American dining culture.",
        origin="United States",
        region="Multiple claims (Louis' Lunch, CT or Lionel Sternberger, CA)",
        image_url="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800&h=600&fit=crop&q=80"
    ),
    
    "Pepperoni pizza": FoodProfile(
        food_id="Pepperoni pizza",
        display_name="Pepperoni Pizza",
        spice_intensity=0.2,
        texture_intensity=0.5,
        preparation_familiarity=0.2,
        richness=0.8,
        psychological_distance=0.2,
        description="A beloved Italian-American creation featuring a yeasted flatbread topped with tomato sauce, mozzarella cheese, and spicy pepperoni slices. The most popular pizza variety in the United States.",
        origin="Italy/United States",
        region="Naples (pizza) / New York (pepperoni style)",
        image_url="https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800&h=600&fit=crop&q=80"
    ),
    
    "Fried chicken": FoodProfile(
        food_id="Fried chicken",
        display_name="Fried Chicken",
        spice_intensity=0.2,
        texture_intensity=0.8,
        preparation_familiarity=0.2,
        richness=0.8,
        psychological_distance=0.2,
        description="Chicken pieces coated in seasoned flour or batter and deep-fried until crispy and golden. A comfort food staple with roots in Southern American cuisine, beloved worldwide for its crunchy exterior and juicy interior.",
        origin="United States",
        region="Southern United States",
        image_url="https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=800&h=600&fit=crop&q=80"
    ),
    
    "Butter chicken": FoodProfile(
        food_id="Butter chicken",
        display_name="Butter Chicken",
        spice_intensity=0.5,
        texture_intensity=0.5,
        preparation_familiarity=0.2,
        richness=0.8,
        psychological_distance=0.2,
        description="A rich, creamy tomato-based curry with tender chicken pieces marinated in yogurt and spices. Invented in Delhi in the 1950s at Moti Mahal restaurant, it has become one of the most popular Indian dishes worldwide.",
        origin="India",
        region="Delhi, North India",
        image_url="https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=800&h=600&fit=crop&q=80"
    ),
    
    "Pasta with red sauce": FoodProfile(
        food_id="Pasta with red sauce",
        display_name="Pasta with Red Sauce",
        spice_intensity=0.2,
        texture_intensity=0.2,
        preparation_familiarity=0.2,
        richness=0.5,
        psychological_distance=0.2,
        description="Classic Italian pasta served with a tomato-based sauce, often featuring garlic, basil, and olive oil. A staple of Italian cuisine that has become a comfort food standard across the globe.",
        origin="Italy",
        region="Southern Italy (Naples region)",
        image_url="https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=800&h=600&fit=crop&q=80"
    ),
    
    "Tacos al pastor": FoodProfile(
        food_id="Tacos al pastor",
        display_name="Tacos al Pastor",
        spice_intensity=0.5,
        texture_intensity=0.5,
        preparation_familiarity=0.5,
        richness=0.5,
        psychological_distance=0.5,
        description="Mexican street tacos featuring marinated pork cooked on a vertical spit, inspired by Lebanese shawarma. Served with pineapple, onions, cilantro, and a corn tortilla, representing the fusion of Middle Eastern and Mexican cuisines.",
        origin="Mexico",
        region="Mexico City",
        image_url="https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=800&h=600&fit=crop&q=80"
    ),
    
    "Ethiopian injera with stew": FoodProfile(
        food_id="Ethiopian injera with stew",
        display_name="Ethiopian Injera with Stew",
        spice_intensity=0.5,
        texture_intensity=0.8,
        preparation_familiarity=0.5,
        richness=0.5,
        psychological_distance=0.5,
        description="A traditional Ethiopian meal featuring spongy sourdough flatbread (injera) served with spiced stews (wot). The injera acts as both plate and utensil, reflecting Ethiopia's unique communal dining culture.",
        origin="Ethiopia",
        region="Ethiopian Highlands",
        image_url="https://images.unsplash.com/photo-1604329760661-e71dc83f8f26?w=800&h=600&fit=crop&q=80"
    ),
    
    "Sushi": FoodProfile(
        food_id="Sushi",
        display_name="Sushi",
        spice_intensity=0.2,
        texture_intensity=0.5,
        preparation_familiarity=0.5,
        richness=0.2,
        psychological_distance=0.5,
        description="A Japanese art form combining vinegared rice with fresh seafood, vegetables, and seaweed. Originating as a preservation method in Southeast Asia, it evolved in Japan over centuries into the refined cuisine enjoyed worldwide today.",
        origin="Japan",
        region="Tokyo & Osaka",
        image_url="https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800&h=600&fit=crop&q=80"
    ),
    
    "Pho": FoodProfile(
        food_id="Pho",
        display_name="Pho",
        spice_intensity=0.2,
        texture_intensity=0.2,
        preparation_familiarity=0.5,
        richness=0.2,
        psychological_distance=0.5,
        description="Vietnam's beloved noodle soup featuring a fragrant beef or chicken broth, rice noodles, and fresh herbs. Developed in the early 20th century in northern Vietnam, it has become the country's most iconic culinary export.",
        origin="Vietnam",
        region="Hanoi, Northern Vietnam",
        image_url="https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=800&h=600&fit=crop&q=80"
    ),
    
    "Falafel wrap": FoodProfile(
        food_id="Falafel wrap",
        display_name="Falafel Wrap",
        spice_intensity=0.2,
        texture_intensity=0.5,
        preparation_familiarity=0.5,
        richness=0.5,
        psychological_distance=0.5,
        description="Deep-fried chickpea or fava bean balls wrapped in pita with vegetables and tahini sauce. A staple of Middle Eastern cuisine with roots tracing back to ancient Egypt, now enjoyed as street food globally.",
        origin="Middle East",
        region="Egypt / Levant",
        image_url="https://images.unsplash.com/photo-1547058881-aa0edd92aab3?w=800&h=600&fit=crop&q=80"
    ),
    
    "Beef tongue tacos": FoodProfile(
        food_id="Beef tongue tacos",
        display_name="Beef Tongue Tacos",
        spice_intensity=0.2,
        texture_intensity=0.8,
        preparation_familiarity=0.8,
        richness=0.5,
        psychological_distance=0.8,
        description="Mexican tacos featuring tender, slow-cooked beef tongue (lengua) served in corn tortillas with onions, cilantro, and salsa. A delicacy in Mexican cuisine that challenges Western diners' comfort zones with organ meat.",
        origin="Mexico",
        region="Central Mexico",
        image_url="https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?w=800&h=600&fit=crop&q=80"
    ),
    
    "Lamb curry": FoodProfile(
        food_id="Lamb curry",
        display_name="Lamb Curry",
        spice_intensity=0.8,
        texture_intensity=0.5,
        preparation_familiarity=0.5,
        richness=0.8,
        psychological_distance=0.5,
        description="A richly spiced South Asian curry featuring tender lamb cooked with aromatic spices, tomatoes, and often yogurt or coconut milk. Popular across India, Pakistan, and Bangladesh with countless regional variations.",
        origin="India/Pakistan",
        region="Kashmir & Hyderabad",
        image_url="https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=800&h=600&fit=crop&q=80"
    ),
    
    "Kimchi stew": FoodProfile(
        food_id="Kimchi stew",
        display_name="Kimchi Stew (Kimchi-jjigae)",
        spice_intensity=0.8,
        texture_intensity=0.5,
        preparation_familiarity=0.8,
        richness=0.5,
        psychological_distance=0.8,
        description="A fiery Korean comfort food made with fermented kimchi, pork, tofu, and vegetables in a spicy broth. A staple of Korean home cooking that exemplifies the bold, fermented flavors central to Korean cuisine.",
        origin="South Korea",
        region="Korea",
        image_url="https://images.unsplash.com/photo-1498654896293-37aacf113fd9?w=800&h=600&fit=crop&q=80"
    ),
    
    "Oxtail stew": FoodProfile(
        food_id="Oxtail stew",
        display_name="Oxtail Stew",
        spice_intensity=0.2,
        texture_intensity=0.8,
        preparation_familiarity=0.8,
        richness=0.8,
        psychological_distance=0.8,
        description="A rich, gelatinous stew made from slow-cooked oxtail (beef tail), vegetables, and aromatics. Popular in Caribbean, Korean, and European cuisines, this dish requires adventurous eaters willing to embrace unconventional cuts.",
        origin="Multiple (Caribbean/Korea/Europe)",
        region="Jamaica, Korea, Italy",
        image_url="https://images.unsplash.com/photo-1547928576-f5208b0488a6?w=800&h=600&fit=crop&q=80"
    ),
    
    "Steak tartare": FoodProfile(
        food_id="Steak tartare",
        display_name="Steak Tartare",
        spice_intensity=0.2,
        texture_intensity=0.5,
        preparation_familiarity=0.8,
        richness=0.5,
        psychological_distance=0.8,
        description="A French delicacy of finely chopped or minced raw beef, seasoned with capers, onions, and a raw egg yolk. Named after Tatar horsemen but refined in Parisian bistros, it challenges diners with its completely raw preparation.",
        origin="France",
        region="Paris, France",
        image_url="https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800&h=600&fit=crop&q=80"
    ),
    
    "Escargot": FoodProfile(
        food_id="Escargot",
        display_name="Escargot",
        spice_intensity=0.2,
        texture_intensity=0.8,
        preparation_familiarity=0.8,
        richness=0.5,
        psychological_distance=0.8,
        description="Cooked land snails, typically served in their shells with garlic-parsley butter. A classic French delicacy that epitomizes haute cuisine while challenging diners unfamiliar with gastropods as food.",
        origin="France",
        region="Burgundy, France",
        image_url="https://images.unsplash.com/photo-1599921841143-819065a55cc6?w=800&h=600&fit=crop&q=80"
    ),
    
    "Haggis": FoodProfile(
        food_id="Haggis",
        display_name="Haggis",
        spice_intensity=0.2,
        texture_intensity=0.8,
        preparation_familiarity=0.8,
        richness=0.8,
        psychological_distance=0.8,
        description="Scotland's national dish made from sheep organs (heart, liver, lungs) mixed with oatmeal, onions, and spices, traditionally encased in a sheep's stomach. A source of fierce national pride and culinary courage.",
        origin="Scotland",
        region="Scottish Highlands",
        image_url="https://images.unsplash.com/photo-1626200419199-391ae4be7a41?w=800&h=600&fit=crop&q=80"
    ),
    
    "Fufu": FoodProfile(
        food_id="Fufu",
        display_name="Fufu",
        spice_intensity=0.2,
        texture_intensity=0.8,
        preparation_familiarity=0.8,
        richness=0.5,
        psychological_distance=0.8,
        description="A starchy West African staple made by pounding boiled cassava, yams, or plantains into a smooth, dough-like consistency. Served with soups and stews, it represents the foundation of many West African meals.",
        origin="West Africa",
        region="Ghana, Nigeria, Cameroon",
        image_url="https://images.unsplash.com/photo-1569562211093-4ed0d0758f12?w=800&h=600&fit=crop&q=80"
    ),
}


# Backward compatibility: FOODS dict with tuple format
FOODS = {
    food_id: profile.to_taste_tuple()
    for food_id, profile in FOOD_REGISTRY.items()
}


# Constants
DIMENSION_NAMES = [
    "spice_intensity",
    "texture_intensity",
    "preparation_familiarity",
    "richness",
    "psychological_distance"
]

VALID_VALUES = [0.2, 0.5, 0.8]


def validate_food_registry():
    """
    Validate that all foods in the registry have complete metadata.
    Should be called on application startup.
    
    Raises:
        ValueError: If any food is missing required metadata or has invalid data.
    """
    errors = []
    
    # Check count
    if len(FOOD_REGISTRY) != 18:
        errors.append(f"Expected exactly 18 foods, found {len(FOOD_REGISTRY)}")
    
    for food_id, profile in FOOD_REGISTRY.items():
        # Check ID consistency
        if profile.food_id != food_id:
            errors.append(f"Food '{food_id}': food_id mismatch ('{profile.food_id}')")
        
        # Check required fields are non-empty
        if not profile.display_name.strip():
            errors.append(f"Food '{food_id}': display_name is empty")
        
        if not profile.description.strip():
            errors.append(f"Food '{food_id}': description is empty")
        
        if not profile.origin.strip():
            errors.append(f"Food '{food_id}': origin is empty")
        
        if not profile.region.strip():
            errors.append(f"Food '{food_id}': region is empty")
        
        if not profile.image_url.strip():
            errors.append(f"Food '{food_id}': image_url is empty")
        
        # Check image URL format
        if not (profile.image_url.startswith('http://') or profile.image_url.startswith('https://')):
            errors.append(f"Food '{food_id}': image_url must be a valid HTTP(S) URL")
        
        # Check taste dimensions are valid
        taste_tuple = profile.to_taste_tuple()
        for i, (dim_name, value) in enumerate(zip(DIMENSION_NAMES, taste_tuple)):
            if value not in VALID_VALUES:
                errors.append(
                    f"Food '{food_id}': {dim_name} has invalid value {value} "
                    f"(must be one of {VALID_VALUES})"
                )
    
    if errors:
        error_msg = "Food registry validation failed:\n" + "\n".join(f"  - {e}" for e in errors)
        raise ValueError(error_msg)
    
    return True


def get_food_metadata(food_id: str) -> dict:
    """
    Get complete metadata for a food item as a dictionary.
    Useful for API responses.
    
    Args:
        food_id: The food identifier (must exist in FOOD_REGISTRY)
    
    Returns:
        Dictionary with all food metadata
    
    Raises:
        KeyError: If food_id is not in the registry
    """
    if food_id not in FOOD_REGISTRY:
        raise KeyError(f"Food '{food_id}' not found in registry. Valid foods: {list(FOOD_REGISTRY.keys())}")
    
    profile = FOOD_REGISTRY[food_id]
    return {
        "food_id": profile.food_id,
        "display_name": profile.display_name,
        "description": profile.description,
        "origin": profile.origin,
        "region": profile.region,
        "image_url": profile.image_url,
        "taste_profile": {
            "spice_intensity": profile.spice_intensity,
            "texture_intensity": profile.texture_intensity,
            "preparation_familiarity": profile.preparation_familiarity,
            "richness": profile.richness,
            "psychological_distance": profile.psychological_distance,
        }
    }


def list_all_foods() -> list:
    """
    Get a list of all food IDs in the registry.
    
    Returns:
        List of food IDs (stable identifiers)
    """
    return list(FOOD_REGISTRY.keys())
