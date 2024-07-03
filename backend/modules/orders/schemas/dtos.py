from typing import Optional, List
from pydantic import BaseModel


class Plate(BaseModel):
    plate_menu_id: int
    quantity: int


class OrderBase(BaseModel):
    plates: Optional[List[Plate]] = []
    user_id: Optional[int] = None
    chef_id: Optional[int] = None
    waiter_id: Optional[int] = None


class RegisterOrder(OrderBase):
    plates: List[Plate]
    user_id: int
    chef_id: int
    waiter_id: int


class UpdateOrder(OrderBase):
    status: str
