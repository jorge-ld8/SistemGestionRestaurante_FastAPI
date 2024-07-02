from fastapi import APIRouter, Body, Depends
from modules.users.commands.delete_user.delete_user_service import DeleteUserService
from modules.users.repositories.user_repository import UserRepository
from shared.core.db.db_connection import get_db
from database import Session, Base
from fastapi import status
from shared.utils.service_result import ServiceResult, handle_result

router = APIRouter()


def delete_user_service():
    db: Session = next(get_db())
    repository = UserRepository(db)
    return DeleteUserService(repository)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK, name="users:delete-user")
async def delete_user(
    user_id: int,
    service: DeleteUserService = Depends(delete_user_service)
):
    result = await service.delete_user(user_id)
    return handle_result(result)
