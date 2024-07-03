from typing import Optional
from pydantic import BaseModel, Field
from modules.plates.schemas.domain import Plate

class PlateMenu(BaseModel):
    id: int
    plate: Plate
    unit_price: int = Field(ge=0)

class Menu(BaseModel):
    id: int
    name: str = Field(min_length=3, max_length=50)
    description: Optional[str] = Field(min_length=3, max_length=255, default=None)
    plates: list[PlateMenu] = []
