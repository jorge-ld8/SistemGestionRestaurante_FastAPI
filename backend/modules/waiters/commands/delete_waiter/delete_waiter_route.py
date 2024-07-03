from fastapi import APIRouter, Body, Depends
from modules.waiters.commands.delete_waiter.delete_waiter_service import DeleteWaiterService
from modules.waiters.repositories.waiter_repository import WaiterRepository
from shared.core.db.db_connection import get_db
from database import Session, Base
from fastapi import status
from modules.users.user_auth.auth_decorators import authenticate_user, authorize_user
from modules.users.user_auth.auth_dependencies import get_current_user

from models import User

from shared.utils.service_result import ServiceResult, handle_result

router = APIRouter()


def delete_waiter_service():
    db: Session = next(get_db())
    repository = WaiterRepository(db)
    return DeleteWaiterService(repository)


@router.delete("/{waiter_id}", status_code=status.HTTP_200_OK, name="waiters:delete-waiter")
@authenticate_user()
@authorize_user(["admin"])
async def delete_waiter(
    waiter_id: int,
    service: DeleteWaiterService = Depends(delete_waiter_service),
    current_user: User = Depends(get_current_user)
):
    result = await service.delete_waiter(waiter_id)
    return handle_result(result)
