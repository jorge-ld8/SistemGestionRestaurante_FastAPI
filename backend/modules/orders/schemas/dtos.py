from typing import Optional, List
from pydantic import BaseModel


class Plate(BaseModel):
    plate_id: int
    quantity: int


class OrderBase(BaseModel):
    pass


class RegisterOrder(OrderBase):
    plates: List[Plate]
    user_id: int
    chef_id: int
    waiter_id: int


class UpdateOrder(OrderBase):
    pass