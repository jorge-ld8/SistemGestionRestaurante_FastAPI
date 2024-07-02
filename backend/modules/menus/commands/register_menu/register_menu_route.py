from fastapi import APIRouter, Body, Depends
from starlette import status

from modules.menus.repositories.write_model.menu_wm_repository import MenuWriteModelRepository as MenuRepository
from modules.menus.schemas.dtos import RegisterMenu
from modules.menus.commands.register_menu.register_menu_service import RegisterMenuService
from shared.core.db.db_connection import get_db
from database import Session, Base

from shared.utils.service_result import handle_result

router = APIRouter()

def register_menu_service():
    db: Session = next(get_db())
    repository = MenuRepository(db)
    return RegisterMenuService(repository)

@router.post("/", status_code=status.HTTP_201_CREATED, name = "menus:register_menu")
async def register_menu(
    menu: RegisterMenu = Body(..., embed=True), 
    service: RegisterMenuService = Depends(register_menu_service)
):
    result = await service.register_menu(menu)
    return handle_result(result)