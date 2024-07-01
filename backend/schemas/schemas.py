from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    first_name: str
    last_name: str
    role: str


class User(UserBase):
    id: int
    is_active: bool
    # items: list[Item] = []

    class Config:
        orm_mode = True