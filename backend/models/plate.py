from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .base import Base


class Plate(Base):
    __tablename__ = 'plates'

    plate_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    is_deleted = Column(Boolean, default=False)

    menus = relationship("PlatesMenu", back_populates="plate")
    ingredients = relationship("PlateIngredient", back_populates="plate")
