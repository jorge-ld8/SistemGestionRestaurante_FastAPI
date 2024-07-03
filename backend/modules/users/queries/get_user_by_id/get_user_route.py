from fastapi import APIRouter, Body, Depends, status

from modules.users.queries.get_user_by_id.get_user_service import GetUserService
from modules.users.repositories.user_repository import UserRepository
from shared.core.db.db_connection import get_db
from database import Session, Base
from shared.utils.service_result import handle_result

router = APIRouter()


def get_user_by_id_service():
    db: Session = next(get_db())
    repository = UserRepository(db)
    return GetUserService(repository)


@router.get("/{user_id}", status_code=status.HTTP_200_OK, name="users:get-user-by-id")
async def get_user_by_id(
    user_id: int,
    service: GetUserService = Depends(get_user_by_id_service)
):
    result = await service.get_user_by_id(user_id)
    return handle_result(result)
