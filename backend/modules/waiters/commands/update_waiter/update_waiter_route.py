from fastapi import APIRouter, Body, Depends
from modules.waiters.commands.update_waiter.update_waiter_service import UpdateWaiterService
from modules.waiters.repositories.waiter_repository import WaiterRepository
from modules.waiters.schemas.dtos import UpdateWaiter
from shared.core.db.db_connection import get_db
from database import Session, Base
from fastapi import status
from shared.utils.service_result import ServiceResult, handle_result

router = APIRouter()


def update_waiter_service():
    db: Session = next(get_db())
    repository = WaiterRepository(db)
    return UpdateWaiterService(repository)


@router.put("/{waiter_id}", status_code=status.HTTP_200_OK, name="waiters:update-waiter")
async def update_waiter(
    waiter_id: int,
    waiter: UpdateWaiter = Body(..., embed=True),
    service: UpdateWaiterService = Depends(update_waiter_service)
):
    result = await service.update_waiter(waiter, waiter_id)
    return handle_result(result)
