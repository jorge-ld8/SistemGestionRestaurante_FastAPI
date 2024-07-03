from fastapi import APIRouter, Body, Depends
from modules.orders.commands.register_order.register_order_route import router as register_order_router
# from modules.orders.queries.get_order_by_id.get_order_route import router as get_order_router
# from modules.orders.commands.update_order.update_order_route import router as update_order_router
# from modules.orders.commands.delete_order.delete_order_route import router as delete_order_router
from modules.orders.commands.change_order.change_order_routes import router as change_order_router

orders_routes = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={404: {"description": "Not found"}},
)

orders_routes.include_router(register_order_router)
# orders_routes.include_router(get_order_router)
# orders_routes.include_router(update_order_router)
# orders_routes.include_router(delete_order_router)
orders_routes.include_router(change_order_router)
