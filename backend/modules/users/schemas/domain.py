from pydantic import BaseModel, Field, constr


class User(BaseModel):
    user_id: int
    user_name: str = Field(min_length=3, max_length=20)
    name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=3, max_length=50)
    role: str = Field(min_length=5, max_length=30)
    password: str
