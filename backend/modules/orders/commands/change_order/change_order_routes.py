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
from modules.orders.commands.change_order.change_order_service import ChangeOrderStatusService

router = APIRouter()


def change_order_service():
    db: Session = next(get_db())
    order_repo = OrderRepository(db)
    return ChangeOrderStatusService(order_repo)


@router.put("/cancel_order/{order_id}", status_code=status.HTTP_200_OK, name="orders:cancel-order")
async def cancel_order(
    order_id: int,
    service: ChangeOrderStatusService = Depends(change_order_service)
):
    result = await service.change_order_status(order_id, "cancelled")
    return handle_result(result)


@router.put("/fulfill_order/{order_id}", status_code=status.HTTP_200_OK, name="orders:fulfill-order")
async def fulfill_order(
    order_id: int,
    service: RegisterOrderService = Depends(change_order_service)
):
    result = await service.change_order_status(order_id, "fulfilled")
    return handle_result(result)

