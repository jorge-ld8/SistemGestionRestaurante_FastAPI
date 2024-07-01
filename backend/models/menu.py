from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .base import Base


class Menu(Base):
    __tablename__ = 'menus'

    menu_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    is_deleted = Column(Boolean, default=False)

    plates = relationship("PlatesMenu", back_populates="menu")

