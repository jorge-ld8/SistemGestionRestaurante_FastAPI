from fastapi import APIRouter, Body, Depends
from modules.waiters.commands.register_waiter.register_waiter_route import router as register_waiter_router
from modules.waiters.queries.get_waiter_by_id.get_waiter_route import router as get_waiter_router
from modules.waiters.commands.update_waiter.update_waiter_route import router as update_waiter_router
from modules.waiters.commands.delete_waiter.delete_waiter_route import router as delete_waiter_router


waiters_routes = APIRouter(
    prefix="/waiters",
    tags=["waiters"],
    responses={404: {"description": "Not found"}},
)

waiters_routes.include_router(register_waiter_router)
waiters_routes.include_router(get_waiter_router)
waiters_routes.include_router(update_waiter_router)
waiters_routes.include_router(delete_waiter_router)

