from fastapi import APIRouter, Body, Depends
from modules.chefs.commands.delete_chef.delete_chef_service import DeleteChefService
from modules.chefs.repositories.chef_repository import ChefRepository
from shared.core.db.db_connection import get_db
from database import Session, Base
from fastapi import status
from shared.utils.service_result import ServiceResult, handle_result
from modules.users.user_auth.auth_decorators import authenticate_user, authorize_user
from modules.users.user_auth.auth_dependencies import get_current_user
from models import User

router = APIRouter()


def delete_chef_service():
    db: Session = next(get_db())
    repository = ChefRepository(db)
    return DeleteChefService(repository)


@router.delete("/{chef_id}", status_code=status.HTTP_200_OK, name="chefs:delete-chef")
@authenticate_user()
@authorize_user(["admin"])
async def delete_chef(
    chef_id: int,
    service: DeleteChefService = Depends(delete_chef_service),
    current_user: User = Depends(get_current_user)
):
    result = await service.delete_chef(chef_id)
    return handle_result(result)
