from sqlalchemy.ext.declarative import declarative_base
from .base import Base, metadata
from .chef import Chef
from .ingredient import Ingredient
from .menu import Menu
from .order import Order
from .order_detail import OrderDetail
from .plate import Plate
from .plate_ingredient import PlateIngredient
from .plate_menu import PlatesMenu
from .user import User
from .waiter import Waiter


