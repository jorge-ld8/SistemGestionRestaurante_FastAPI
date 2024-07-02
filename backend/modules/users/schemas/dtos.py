from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    user_name: Optional[str] = None
    role: Optional[str] = None


class RegisterUser(UserBase):
    name: str
    last_name: str
    user_name: str
    role: str


class UpdateUser(UserBase):
    pass