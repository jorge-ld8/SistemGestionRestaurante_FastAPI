from typing import Optional
from pydantic import BaseModel

# class PlateBase(BaseModel):
#     name: Optional[str] = None
#     description: Optional[str] = None
#     ingredients: Optional[list[Ingredient]] = None

class Ingredient(BaseModel):
    ingredientId: int
    quantity: float

class RegisterPlate(BaseModel):
    name: str
    description: Optional[str] = None
    ingredients: list[Ingredient]

class UpdatePlate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None