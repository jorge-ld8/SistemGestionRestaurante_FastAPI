from fastapi import APIRouter, Depends
from starlette import status

from modules.menus.repositories.write_model.menu_wm_repository import MenuWriteModelRepository as MenuRepository
from modules.menus.commands.delete_menu.delete_menu_service import DeleteMenuService
from shared.core.db.db_connection import get_db
from database import Session, Base

from shared.utils.service_result import handle_result

router = APIRouter()

def delete_menu_service():
    db: Session = next(get_db())
    repository = MenuRepository(db)
    return DeleteMenuService(repository)

@router.delete("/{menu_id}", status_code=status.HTTP_200_OK, name = "menus:delete_menu")
async def delete_menu(
    menu_id: int,
    service: DeleteMenuService = Depends(delete_menu_service)
):
    result = await service.delete_menu(menu_id)
    return handle_result(result)
