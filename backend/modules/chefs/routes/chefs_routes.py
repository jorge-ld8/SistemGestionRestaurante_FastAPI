from fastapi import APIRouter, Body, Depends
from modules.chefs.commands.register_chef.register_chef_route import router as register_chef_router
from modules.chefs.queries.get_chef_by_id.get_chef_route import router as get_chef_router
from modules.chefs.commands.update_chef.update_chef_route import router as update_chef_router
from modules.chefs.commands.delete_chef.delete_chef_route import router as delete_chef_router


chefs_routes = APIRouter(
    prefix="/chefs",
    tags=["chefs"],
    responses={404: {"description": "Not found"}},
)

chefs_routes.include_router(register_chef_router)
chefs_routes.include_router(get_chef_router)
chefs_routes.include_router(update_chef_router)
chefs_routes.include_router(delete_chef_router)

