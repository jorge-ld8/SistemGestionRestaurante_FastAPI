from fastapi import APIRouter
from modules.users import users_router
from modules.ingredients.routes.ingredients_routes import ingredients_routes
router = APIRouter()

# router.include_router(users_router)
 
router.include_router(ingredients_routes)
