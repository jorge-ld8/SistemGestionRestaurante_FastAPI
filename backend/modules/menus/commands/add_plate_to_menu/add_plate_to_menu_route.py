from fastapi import APIRouter, Body, Depends
from starlette import status

from modules.menus.repositories.write_model.menu_wm_repository import MenuWriteModelRepository as MenuRepository
from modules.plates.repositories.write_model.plate_wm_repository import PlateWriteModelRepository as PlateRepository
from modules.menus.schemas.dtos import AddPlateToMenu
from modules.menus.commands.add_plate_to_menu.add_plate_to_menu_service import AddPlateToMenuService
from shared.core.db.db_connection import get_db
from database import Session, Base
from modules.users.user_auth.auth_decorators import authenticate_user, authorize_user
from modules.users.user_auth.auth_dependencies import get_current_user

from models import User

from shared.utils.service_result import handle_result

router = APIRouter()

def add_plate_to_menu_service():
    db: Session = next(get_db())
    menu_repository = MenuRepository(db)
    plate_repository = PlateRepository(db)
    return AddPlateToMenuService(menu_repository, plate_repository)

@router.post("/{menu_id}", status_code=status.HTTP_201_CREATED, name = "menus:add_plate_to_menu")
@authenticate_user()
@authorize_user(["admin"])
async def add_plate_to_menu(
    menu_id:int,
    plate: AddPlateToMenu = Body(..., embed=True), 
    service: AddPlateToMenuService = Depends(add_plate_to_menu_service),
    current_user: User = Depends(get_current_user)
):
    result = await service.add_plate_to_menu(menu_id, plate)
    return handle_result(result)
