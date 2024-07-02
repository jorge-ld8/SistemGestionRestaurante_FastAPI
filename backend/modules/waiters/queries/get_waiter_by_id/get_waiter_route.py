from fastapi import APIRouter, Body, Depends, status

from modules.waiters.queries.get_waiter_by_id.get_waiter_service import GetWaiterService
from modules.waiters.repositories.waiter_repository import WaiterRepository
from shared.core.db.db_connection import get_db
from database import Session, Base
from shared.utils.service_result import handle_result

router = APIRouter()


def get_waiter_by_id_service():
    db: Session = next(get_db())
    repository = WaiterRepository(db)
    return GetWaiterService(repository)


@router.get("/{waiter_id}", status_code=status.HTTP_200_OK)
async def get_waiter_by_id(
    waiter_id: int,
    service: GetWaiterService = Depends(get_waiter_by_id_service)
):
    result = await service.get_waiter_by_id(waiter_id)
    return handle_result(result)