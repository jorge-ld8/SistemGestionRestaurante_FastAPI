from fastapi import APIRouter
from modules.users import users_router
from modules.ingredients.routes.ingredients_routes import ingredients_routes
from modules.plates.routes.plates_routes import plates_routes
from modules.menus.routes.menus_routes import menus_routes
router = APIRouter()

# router.include_router(users_router)
 
router.include_router(ingredients_routes)
router.include_router(plates_routes)
router.include_router(menus_routes)