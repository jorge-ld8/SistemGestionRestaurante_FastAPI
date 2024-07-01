from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class OrderDetail(Base):
    __tablename__ = 'order_details'

    order_detail_id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    plates_menu_id = Column(Integer, ForeignKey("plates_menus.plate_menu_id"), nullable=False)

    order = relationship("Order", back_populates="order_details")
    plate_menu = relationship("PlatesMenu", back_populates="order_details")