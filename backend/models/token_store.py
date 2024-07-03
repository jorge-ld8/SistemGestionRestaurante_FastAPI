from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.orm import relationship
from .base import Base


class TokenStore(Base):
    __tablename__ = 'token_store'

    id = Column(Integer, primary_key=True)
    token = Column(String, unique=True, nullable=False)
    created_at = Column(Date, nullable=False)
