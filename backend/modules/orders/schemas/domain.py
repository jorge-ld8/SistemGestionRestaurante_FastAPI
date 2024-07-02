from typing import Optional, List
from pydantic import BaseModel, Field
from sqlalchemy import DateTime

from backend.modules.orders.schemas.dtos import Plate


class Order(BaseModel):
    plates: List[Plate]
    user_id: int = Field()
    chef_id: int = Field()
    waiter_id: int = Field()
    # datetime: DateTime = Field()
    # status: str = Field()
    total: str = Field()