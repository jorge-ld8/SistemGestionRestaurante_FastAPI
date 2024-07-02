from fastapi import APIRouter

from modules.plates.commands.register_plate.register_plate_route import router as register_plate_router
from modules.plates.commands.update_plate.update_plate_route import router as update_plate_router
from modules.plates.commands.delete_plate.delete_plate_route import router as delete_plate_router

plates_routes = APIRouter(
    prefix="/plates",
    tags=["plates"],
    responses={404: {"description": "Not found"}},
)

plates_routes.include_router(register_plate_router)

plates_routes.include_router(update_plate_router)

plates_routes.include_router(delete_plate_router)