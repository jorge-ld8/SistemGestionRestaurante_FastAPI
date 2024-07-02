from typing import Optional
from pydantic import BaseModel

class IngredientBase(BaseModel):
    name: Optional[str] = None
    stock: Optional[float] = None
    description: Optional[str] = None
    unit: Optional[str] = None

class RegisterIngredient(IngredientBase):
    name: str
    stock: float
    unit: str

class UpdateIngredient(IngredientBase):
    pass