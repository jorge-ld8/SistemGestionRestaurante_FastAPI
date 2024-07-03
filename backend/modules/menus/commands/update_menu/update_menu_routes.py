from fastapi import APIRouter, Body, Depends
from starlette import status

from modules.menus.repositories.write_model.menu_wm_repository import MenuWriteModelRepository as MenuRepository
from modules.menus.schemas.dtos import UpdateMenu
from modules.menus.commands.update_menu.update_menu_service import UpdateMenuService
from shared.core.db.db_connection import get_db
from database import Session, Base
from modules.users.user_auth.auth_decorators import authenticate_user, authorize_user
from modules.users.user_auth.auth_dependencies import get_current_user

from models import User

from shared.utils.service_result import handle_result

router = APIRouter()

def update_menu_service():
    db: Session = next(get_db())
    repository = MenuRepository(db)
    return UpdateMenuService(repository)

@router.put("/{menu_id}", status_code=status.HTTP_200_OK, name = "menus:update_menu")
@authenticate_user()
@authorize_user(["admin"])
async def update_menu(
    menu_id: int,
    menu: UpdateMenu = Body(..., embed=True), 
    service: UpdateMenuService = Depends(update_menu_service),
    current_user: User = Depends(get_current_user)
):
    result = await service.update_menu(menu_id, menu)
    return handle_result(result)
