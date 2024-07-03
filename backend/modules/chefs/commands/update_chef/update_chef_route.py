from fastapi import APIRouter, Body, Depends
from modules.chefs.commands.update_chef.update_chef_service import UpdateChefService
from modules.chefs.repositories.chef_repository import ChefRepository
from modules.chefs.schemas.dtos import UpdateChef
from shared.core.db.db_connection import get_db
from database import Session, Base
from fastapi import status
from shared.utils.service_result import ServiceResult, handle_result
from modules.users.user_auth.auth_decorators import authenticate_user, authorize_user
from modules.users.user_auth.auth_dependencies import get_current_user

from backend.models import User

router = APIRouter()


def update_chef_service():
    db: Session = next(get_db())
    repository = ChefRepository(db)
    return UpdateChefService(repository)


@router.put("/{chef_id}", status_code=status.HTTP_200_OK, name="chefs:update-chef")
@authenticate_user()
@authorize_user(["admin"])
async def update_chef(
    chef_id: int,
    chef: UpdateChef = Body(..., embed=True),
    service: UpdateChefService = Depends(update_chef_service),
    current_user: User = Depends(get_current_user)
):
    result = await service.update_chef(chef, chef_id)
    return handle_result(result)
