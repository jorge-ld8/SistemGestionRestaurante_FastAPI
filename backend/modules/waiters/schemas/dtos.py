from typing import Optional
from pydantic import BaseModel


class WaiterBase(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None


class RegisterWaiter(WaiterBase):
    name: str
    last_name: str


class UpdateWaiter(WaiterBase):
    pass