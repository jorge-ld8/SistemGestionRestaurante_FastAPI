import enum
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from .base import Base


class Unit(enum.Enum):
    grams = "grams"
    litres = "litres"


class Ingredient(Base):
    __tablename__ = 'ingredients'

    ingredient_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    stock = Column(Float, nullable=False)
    unit = Column(String, default=Unit.grams)
    description = Column(String)
    is_deleted = Column(Boolean, default=False)

    plates = relationship("PlateIngredient", back_populates="ingredient")

