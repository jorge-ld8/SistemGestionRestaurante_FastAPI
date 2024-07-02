from typing import Optional
from pydantic import BaseModel, Field

from modules.ingredients.schemas.domain import Ingredient

class PlateIngredient(BaseModel):
    ingredient: Ingredient
    quantity: float

class Plate(BaseModel):
    id: int
    name: str = Field(min_length=3, max_length=50)
    description: Optional[str] = Field(min_length=3, max_length=255, default=None)
    # ingredients: Optional[list[Ingredient]] = None
    ingredients: list[PlateIngredient] = []