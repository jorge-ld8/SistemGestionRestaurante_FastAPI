from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base
import enum


class Status(enum.Enum):
    recieved = "Recieved"
    preparing = "Preparing"
    ready = "Ready"
    fulfilled = "Fulfilled"
    canceled = "Canceled"
    transporting = "Transporting"


class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True)
    estado = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False)
    total = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    chef_id = Column(Integer, ForeignKey("chefs.chef_id"), nullable=False)
    waiter_id = Column(Integer, ForeignKey("waiters.waiter_id"), nullable=False)
    is_deleted = Column(Boolean, default=False)

    user = relationship("User", back_populates="orders")
    chef = relationship("Chef", back_populates="orders")
    waiter = relationship("Waiter", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order")
