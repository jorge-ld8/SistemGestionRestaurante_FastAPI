from typing import Optional
from pydantic import BaseModel

class RegisterMenu(BaseModel):
    name: str
    description: Optional[str] = None

class UpdateMenu(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class AddPlateToMenu(BaseModel):
    plate_id: int
    unit_price: int

class CheckPlateAvailability(BaseModel):
    plate_menu_id: int
    quantity: int

class UpdatePlatePriceOfMenu(BaseModel):
    unit_price: int
