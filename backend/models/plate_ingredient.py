from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class PlateIngredient(Base):
    __tablename__ = 'plate_ingredients'

    plate_ingredient_id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer, nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.ingredient_id"), nullable=False)
    plate_id = Column(Integer, ForeignKey("plates.plate_id"), nullable=False)

    ingredient = relationship("Ingredient", back_populates="plates")
    plate = relationship("Plate", back_populates="ingredients")