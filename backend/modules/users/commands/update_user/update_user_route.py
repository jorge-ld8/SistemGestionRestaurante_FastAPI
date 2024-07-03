from fastapi import APIRouter, Body, Depends
from modules.users.commands.update_user.update_user_service import UpdateUserService
from modules.users.repositories.user_repository import UserRepository
from modules.users.schemas.dtos import UpdateUser
from shared.core.db.db_connection import get_db
from database import Session, Base
from fastapi import status
from shared.utils.service_result import ServiceResult, handle_result

router = APIRouter()


def update_user_service():
    db: Session = next(get_db())
    repository = UserRepository(db)
    return UpdateUserService(repository)


@router.put("/{user_id}", status_code=status.HTTP_200_OK, name="users:update-user")
async def update_user(
    user_id: int,
    user: UpdateUser = Body(..., embed=True),
    service: UpdateUserService = Depends(update_user_service)
):
    result = await service.update_user(user)
    return handle_result(result)
