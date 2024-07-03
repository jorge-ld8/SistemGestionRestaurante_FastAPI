from fastapi import APIRouter, Body, Depends
from starlette import status

from modules.orders.commands.register_order.register_order_service import RegisterOrderService
from modules.orders.repositories.order_repository import OrderRepository
from modules.orders.schemas.dtos import RegisterOrder
from shared.core.db.db_connection import get_db
from database import Session, Base
from shared.utils.service_result import ServiceResult, handle_result
from modules.users.repositories.user_repository import UserRepository
from modules.waiters.repositories.waiter_repository import WaiterRepository
from modules.chefs.repositories.chef_repository import ChefRepository
from modules.menus.repositories.write_model.menu_wm_repository import MenuWriteModelRepository
from modules.plates.repositories.write_model.plate_wm_repository import PlateWriteModelRepository

from modules.ingredients.repositories.ingredient_repository import IngredientRepository

router = APIRouter()


def register_order_service():
    db: Session = next(get_db())
    order_repo = OrderRepository(db)
    user_repo = UserRepository(db)
    waiter_repo = WaiterRepository(db)
    chef_repo = ChefRepository(db)
    menu_repo = MenuWriteModelRepository(db)
    plate_repo = PlateWriteModelRepository(db)
    ingredient_repo = IngredientRepository(db)
    return RegisterOrderService(order_repo, user_repo, waiter_repo, chef_repo, menu_repo, plate_repo, ingredient_repo)


@router.post("/", status_code=status.HTTP_201_CREATED, name="orders:register-order")
async def register_order(
    order: RegisterOrder = Body(..., embed=True),
    service: RegisterOrderService = Depends(register_order_service)
):
    result = await service.register_order(order)
    return handle_result(result)