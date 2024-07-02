from fastapi import APIRouter, Body, Depends
from starlette import status
from modules.waiters.repositories.waiter_repository import WaiterRepository
from modules.waiters.schemas.dtos import RegisterWaiter
from modules.waiters.commands.register_waiter.register_waiter_service import RegisterWaiterService
from shared.core.db.db_connection import get_db
from database import Session, Base

from shared.utils.service_result import ServiceResult, handle_result

router = APIRouter()


def register_waiter_service():
    db: Session = next(get_db())
    repository = WaiterRepository(db)
    return RegisterWaiterService(repository)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def register_waiter(
    waiter: RegisterWaiter = Body(..., embed=True), 
    service: RegisterWaiterService = Depends(register_waiter_service)
):
    result = await service.register_waiter(waiter)
    return handle_result(result)
