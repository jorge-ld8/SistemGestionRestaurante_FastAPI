from fastapi import APIRouter, Depends
from starlette import status

from modules.menus.repositories.write_model.menu_wm_repository import MenuWriteModelRepository as MenuRepository
from modules.menus.commands.remove_plate_from_menu.remove_plate_from_menu_service import RemovePlateFromMenuService
from shared.core.db.db_connection import get_db
from database import Session, Base
from modules.users.user_auth.auth_decorators import authenticate_user, authorize_user
from modules.users.user_auth.auth_dependencies import get_current_user

from models import User

from shared.utils.service_result import handle_result

router = APIRouter()

def remove_plate_from_menu_service():
    db: Session = next(get_db())
    repository = MenuRepository(db)
    return RemovePlateFromMenuService(repository)

@router.delete("/{menu_id}/plate/{plate_id}", status_code=status.HTTP_200_OK, name = "menus:remove_plate_from_menu")
@authenticate_user()
@authorize_user(["admin"])
async def remove_plate_from_menu(
    menu_id: int, 
    plate_id: int,
    service: RemovePlateFromMenuService = Depends(remove_plate_from_menu_service),
    current_user: User = Depends(get_current_user)
):
    result = await service.remove_plate_from_menu(menu_id, plate_id)
    return handle_result(result)