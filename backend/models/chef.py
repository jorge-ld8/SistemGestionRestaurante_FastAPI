from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .base import Base


class Chef(Base):
    __tablename__ = 'chefs'

    chef_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_deleted = Column(Boolean, default=False)

    orders = relationship("Order", back_populates="chef")
