from fastapi import APIRouter, Body, Depends
from backend.modules.orders.commands.register_order.register_order_service import RegisterOrderService
from backend.modules.orders.repositories.order_repository import OrderRepository
from backend.modules.orders.schemas.dtos import RegisterOrder
from backend.shared.core.db.db_connection import get_db
from backend.database import Session, Base
from backend.shared.utils.service_result import ServiceResult, handle_result

router = APIRouter()


def register_order_service():
    db: Session = next(get_db())
    repository = OrderRepository(db)
    return RegisterOrderService(repository)


@router.post("/", status_code=201)
async def register_order(
    order: RegisterOrder = Body(..., embed=True),
    service: RegisterOrderService = Depends(register_order_service)
):
    result = await service.register_order(order)
    return handle_result(result)