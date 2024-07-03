from typing import Optional, List
from pydantic import BaseModel, Field
from modules.orders.schemas.dtos import Plate
from datetime import datetime


class OrderDetail(BaseModel):
    quantity: int
    plate_id: int
    plate_menu_id: int


class Order(BaseModel):
    order_id: int
    user_id: int
    chef_id: int
    waiter_id: int
    datetime: datetime
    status: str = Field(regex="^(preparing|fulfilled|cancelled)$")
    total: float = Field(gt=0)
    order_details: List[OrderDetail]




