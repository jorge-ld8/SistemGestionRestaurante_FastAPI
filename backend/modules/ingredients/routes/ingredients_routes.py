from fastapi import APIRouter, Body, Depends

from modules.ingredients.commands.register_ingredient.register_ingredient_route import router as register_ingredient_router
from modules.ingredients.commands.update_ingredient.update_ingredient_route import router as update_ingredient_router
from modules.ingredients.queries.get_ingredient_by_id.get_ingredient_by_id_route import router as get_ingredient_by_id_router
from modules.ingredients.commands.delete_ingredient.delete_ingredient_route import router as delete_ingredient_router
from modules.ingredients.commands.adjust_ingredient_stock.adjust_ingredient_stock_route import router as adjust_ingredient_stock_router

ingredients_routes = APIRouter(
    prefix="/ingredients",
    tags=["ingredients"],
    responses={404: {"description": "Not found"}},
)

ingredients_routes.include_router(register_ingredient_router)

ingredients_routes.include_router(update_ingredient_router)

ingredients_routes.include_router(get_ingredient_by_id_router)

ingredients_routes.include_router(delete_ingredient_router)

ingredients_routes.include_router(adjust_ingredient_stock_router)
