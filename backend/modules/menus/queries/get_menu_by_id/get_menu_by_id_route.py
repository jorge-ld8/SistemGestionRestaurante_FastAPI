from fastapi import APIRouter, Body, Depends
from starlette import status

from modules.menus.repositories.read_model.menu_rm_repository import MenuReadModelRepository as MenuRepository
from modules.menus.queries.get_menu_by_id.get_menu_by_id_service import GetMenuByIdService
from shared.core.db.db_connection import get_db
from database import Session, Base
from modules.users.user_auth.auth_decorators import authenticate_user, authorize_user
from modules.users.user_auth.auth_dependencies import get_current_user

from models import User

from shared.utils.service_result import handle_result

router = APIRouter()

def get_menu_by_id_service():
    db: Session = next(get_db())
    repository = MenuRepository(db)
    return GetMenuByIdService(repository)

@router.get("/{menu_id}", status_code=status.HTTP_201_CREATED, name = "menus:get_menu_by_id")
@authenticate_user()
@authorize_user(["admin"])
async def get_menu_by_id(
    menu_id: int, 
    service: GetMenuByIdService = Depends(get_menu_by_id_service),
    current_user: User = Depends(get_current_user)
):
    result = await service.get_menu_by_id(menu_id)
    return handle_result(result)