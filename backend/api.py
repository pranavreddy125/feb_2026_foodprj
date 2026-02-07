#!/usr/bin/env python3
"""
FastAPI server for Food Personality Backend
Exposes POST /assign_to_rings endpoint
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from typing import List, Optional, Set

from backend import (
    UserTasteVector,
    Archetype,
    assign_to_rings,
    VALID_VALUES,
    FOODS,
    validate_food_registry,
    get_food_metadata,
    list_all_foods
)

app = FastAPI(title="Food Personality API", version="1.0.1")

# Validate food registry on startup
@app.on_event("startup")
async def startup_validation():
    """Validate food registry on application startup."""
    try:
        validate_food_registry()
        print("✅ Food registry validated: 18 foods with complete metadata")
    except ValueError as e:
        print(f"❌ Food registry validation failed:\n{e}")
        raise

# CORS configuration - allow frontend on localhost:8081
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8081",
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AssignRingsRequest(BaseModel):
    """Request payload for /assign_to_rings endpoint"""
    spice_intensity: float
    texture_intensity: float
    preparation_familiarity: float
    richness: float
    psychological_distance: float
    dislikes: Optional[List[str]] = []
    archetypes: Optional[List[str]] = []

    @field_validator('spice_intensity', 'texture_intensity', 'preparation_familiarity', 'richness', 'psychological_distance')
    @classmethod
    def validate_dimensions(cls, v):
        if v not in VALID_VALUES:
            raise ValueError(f'Value must be one of {VALID_VALUES}')
        return v

    @field_validator('dislikes', mode='before')
    @classmethod
    def validate_dislikes(cls, v):
        if v is None:
            return []
        valid_foods = set(FOODS.keys())
        invalid = [f for f in v if f not in valid_foods]
        if invalid:
            raise ValueError(f'Invalid food names: {invalid}')
        return v

    @field_validator('archetypes', mode='before')
    @classmethod
    def validate_archetypes(cls, v):
        if v is None:
            return []
        valid_archetypes = {arch.value for arch in Archetype}
        invalid = [a for a in v if a not in valid_archetypes]
        if invalid:
            raise ValueError(f'Invalid archetypes: {invalid}')
        return v


@app.post("/assign_to_rings")
def assign_to_rings_endpoint(request: AssignRingsRequest):
    """
    Compute comfort rings for the given taste vector.
    
    Returns:
    - ring_0, ring_1, ring_2: lists of foods with distances
    - personality: primary + secondary personality with confidence scores
    - ring_thresholds: the distance thresholds used
    """
    try:
        # Build user taste vector
        user_vector = UserTasteVector(
            spice_intensity=request.spice_intensity,
            texture_intensity=request.texture_intensity,
            preparation_familiarity=request.preparation_familiarity,
            richness=request.richness,
            psychological_distance=request.psychological_distance,
        )

        # Convert archetypes from strings to Archetype enums
        archetype_set: Set[Archetype] = set()
        for arch_str in request.archetypes:
            archetype_set.add(Archetype(arch_str))

        # Call backend logic
        assignment = assign_to_rings(
            user_vector=user_vector,
            dislikes=set(request.dislikes),
            archetypes=archetype_set
        )

        # Format response
        def format_food_distance(fd):
            metadata = get_food_metadata(fd.food_name)
            return {
                "food_name": fd.food_name,
                "display_name": metadata["display_name"],
                "distance": fd.distance,
                "ring": fd.ring,
                "dimension_contributions": fd.dimension_contributions,
                "image_url": metadata["image_url"],
                "description": metadata["description"],
                "origin": metadata["origin"],
                "region": metadata["region"],
            }

        return {
            "ring_0": [format_food_distance(fd) for fd in assignment.ring_0],
            "ring_1": [format_food_distance(fd) for fd in assignment.ring_1],
            "ring_2": [format_food_distance(fd) for fd in assignment.ring_2],
            "personality": {
                "primary_personality": assignment.personality.primary_personality,
                "secondary_personality": assignment.personality.secondary_personality,
                "confidence_primary": assignment.personality.confidence_primary,
                "confidence_secondary": assignment.personality.confidence_secondary,
                "explanation": assignment.personality.explanation,
            },
            "ring_thresholds": list(assignment.ring_thresholds),
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "service": "Food Personality API",
        "version": "1.0.1",
        "status": "ok",
        "foods_count": len(list_all_foods()),
    }


@app.get("/foods")
def get_all_foods():
    """
    Get list of all available foods with their IDs.
    
    Returns:
        List of food IDs
    """
    return {
        "foods": list_all_foods(),
        "count": len(list_all_foods())
    }


@app.get("/foods/{food_id}")
def get_food(food_id: str):
    """
    Get complete metadata for a specific food.
    
    Args:
        food_id: The food identifier
    
    Returns:
        Complete food metadata including taste profile, description, origin, image URL
    
    Raises:
        HTTPException: 404 if food not found
    """
    try:
        metadata = get_food_metadata(food_id)
        return metadata
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
