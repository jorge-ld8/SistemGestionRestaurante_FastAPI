from fastapi import APIRouter
from modules.ingredients.routes.ingredients_routes import ingredients_routes
from modules.chefs.routes.chefs_routes import chefs_routes
from modules.waiters.routes.waiters_routes import waiters_routes
from modules.users.routes.users_routes import users_routes

from modules.orders.routes.order_routes import orders_routes
# from modules.orders.routes.orders_routes import orders_routes


router = APIRouter()

router.include_router(ingredients_routes)
router.include_router(chefs_routes)
router.include_router(waiters_routes)
router.include_router(users_routes)
router.include_router(orders_routes)

