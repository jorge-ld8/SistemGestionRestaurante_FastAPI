from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class PlatesMenu(Base):
    __tablename__ = 'plates_menus'

    plate_menu_id = Column(Integer, primary_key=True, autoincrement=True)
    plate_id = Column(Integer, ForeignKey("plates.plate_id"), nullable=False)
    menu_id = Column(Integer, ForeignKey("menus.menu_id"), nullable=False)
    unit_price = Column(Integer, nullable=False)

    plate = relationship("Plate", back_populates="menus")
    menu = relationship("Menu", back_populates="plates")
    order_details = relationship("OrderDetail", back_populates="plate_menu")
