from pydantic import BaseModel, Field


class Waiter(BaseModel):
    waiter_id: int
    name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=3, max_length=50)