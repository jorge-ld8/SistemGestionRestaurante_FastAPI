from fastapi import APIRouter, Depends, Body
from starlette import status

from modules.menus.repositories.write_model.menu_wm_repository import MenuWriteModelRepository as MenuRepository
from modules.menus.commands.update_plate_price_of_menu.update_plate_price_of_menu_service import UpdatePlatePriceOfMenuService
from modules.menus.schemas.dtos import UpdatePlatePriceOfMenu
from shared.core.db.db_connection import get_db
from database import Session, Base
from modules.users.user_auth.auth_decorators import authenticate_user, authorize_user
from modules.users.user_auth.auth_dependencies import get_current_user

from models import User

from shared.utils.service_result import handle_result

router = APIRouter()

def update_plate_price_of_menu_service():
    db: Session = next(get_db())
    repository = MenuRepository(db)
    return UpdatePlatePriceOfMenuService(repository)

@router.put("/plates/{plate_menu_id}", status_code=status.HTTP_200_OK, name = "menus:update_plate_price_of_menu")
@authenticate_user()
@authorize_user(["admin"])
async def update_plate_price_of_menu(
    plate_menu_id: int, 
    dto: UpdatePlatePriceOfMenu = Body(...),
    service: UpdatePlatePriceOfMenuService = Depends(update_plate_price_of_menu_service),
    current_user: User = Depends(get_current_user)
):
    result = await service.update_plate_price_of_menu(plate_menu_id, dto)
    return handle_result(result)