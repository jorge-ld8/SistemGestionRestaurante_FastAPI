from typing import Optional
from pydantic import BaseModel


class ChefBase(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None


class RegisterChef(ChefBase):
    name: str
    last_name: str


class UpdateChef(ChefBase):
    pass