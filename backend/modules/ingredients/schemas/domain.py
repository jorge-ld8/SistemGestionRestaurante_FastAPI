from typing import Optional
from pydantic import BaseModel, Field

class Ingredient(BaseModel):
    id: int
    name: str = Field(min_length=3, max_length=50)
    stock: float = Field(gt=0)
    unit: str = Field(regex="^(grams|litres)$")
    description: Optional[str] = Field(min_length=3, max_length=255, default=None)