from fastapi import APIRouter
from modules.users import users_router
from modules.ingredients.routes.ingredients_routes import ingredients_routes
from modules.chefs.routes.chefs_routes import chefs_routes
from modules.waiters.routes.waiters_routes import waiters_routes


router = APIRouter()
# router.include_router(users_router)
 
router.include_router(ingredients_routes)
router.include_router(chefs_routes)
router.include_router(waiters_routes)
