"""
Fixed food data for the system.
Episode: cursor_foodapp

18 foods with semantic profiles across 5 dimensions.
"""

FOODS = {
    "Cheeseburger": (0.2, 0.5, 0.2, 0.8, 0.2),
    "Pepperoni pizza": (0.2, 0.5, 0.2, 0.8, 0.2),
    "Fried chicken": (0.2, 0.8, 0.2, 0.8, 0.2),
    "Butter chicken": (0.5, 0.5, 0.2, 0.8, 0.2),
    "Pasta with red sauce": (0.2, 0.2, 0.2, 0.5, 0.2),
    "Tacos al pastor": (0.5, 0.5, 0.5, 0.5, 0.5),
    "Ethiopian injera with stew": (0.5, 0.8, 0.5, 0.5, 0.5),
    "Sushi": (0.2, 0.5, 0.5, 0.2, 0.5),
    "Pho": (0.2, 0.2, 0.5, 0.2, 0.5),
    "Falafel wrap": (0.2, 0.5, 0.5, 0.5, 0.5),
    "Beef tongue tacos": (0.2, 0.8, 0.8, 0.5, 0.8),
    "Lamb curry": (0.8, 0.5, 0.5, 0.8, 0.5),
    "Kimchi stew": (0.8, 0.5, 0.8, 0.5, 0.8),
    "Oxtail stew": (0.2, 0.8, 0.8, 0.8, 0.8),
    "Steak tartare": (0.2, 0.5, 0.8, 0.5, 0.8),
    "Escargot": (0.2, 0.8, 0.8, 0.5, 0.8),
    "Haggis": (0.2, 0.8, 0.8, 0.8, 0.8),
    "Fufu": (0.2, 0.8, 0.8, 0.5, 0.8)
}

DIMENSION_NAMES = [
    "spice_intensity",
    "texture_intensity",
    "preparation_familiarity",
    "richness",
    "psychological_distance"
]

VALID_VALUES = [0.2, 0.5, 0.8]
