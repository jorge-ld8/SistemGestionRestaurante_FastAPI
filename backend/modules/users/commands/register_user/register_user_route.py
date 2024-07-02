from fastapi import APIRouter, Body, Depends
from starlette import status
from modules.users.repositories.user_repository import UserRepository
from modules.users.schemas.dtos import RegisterUser
from modules.users.commands.register_user.register_user_service import RegisterUserService
from shared.core.db.db_connection import get_db
from database import Session, Base

from shared.utils.service_result import ServiceResult, handle_result

router = APIRouter()


def register_user_service():
    db: Session = next(get_db())
    repository = UserRepository(db)
    return RegisterUserService(repository)


@router.post("/", status_code=status.HTTP_201_CREATED, name="users:register-user")
async def register_user(
    user: RegisterUser = Body(..., embed=True), 
    service: RegisterUserService = Depends(register_user_service)
):
    result = await service.register_user(user)
    return handle_result(result)
