from fastapi import APIRouter, Body, Depends
from modules.users.commands.register_user.register_user_route import router as register_user_router
from modules.users.queries.get_user_by_id.get_user_route import router as get_user_router
from modules.users.commands.update_user.update_user_route import router as update_user_router
from modules.users.commands.delete_user.delete_user_route import router as delete_user_router
from modules.users.user_auth.auth_routes import router as auth_router

users_routes = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

users_routes.include_router(register_user_router)
users_routes.include_router(get_user_router)
users_routes.include_router(update_user_router)
users_routes.include_router(delete_user_router)
users_routes.include_router(auth_router)


