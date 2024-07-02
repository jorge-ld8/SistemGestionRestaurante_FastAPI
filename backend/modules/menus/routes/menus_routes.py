from fastapi import APIRouter

from modules.menus.commands.register_menu.register_menu_route import router as register_menu_router
from modules.menus.commands.update_menu.update_menu_routes import router as update_menu_router
from modules.menus.commands.delete_menu.delete_menu_routes import router as delete_menu_router
from modules.menus.commands.add_plate_to_menu.add_plate_to_menu_route import router as add_plate_to_menu_router
from modules.menus.commands.remove_plate_from_menu.remove_plate_from_menu_route import router as remove_plate_from_menu_router

menus_routes = APIRouter(
    prefix="/menus",
    tags=["menus"],
    responses={404: {"description": "Not found"}},
)

menus_routes.include_router(register_menu_router)
menus_routes.include_router(update_menu_router)
menus_routes.include_router(delete_menu_router)
menus_routes.include_router(add_plate_to_menu_router)
menus_routes.include_router(remove_plate_from_menu_router)
