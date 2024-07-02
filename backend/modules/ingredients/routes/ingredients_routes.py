from fastapi import APIRouter, Body, Depends

from modules.ingredients.commands.register_ingredient.register_ingredient_route import router as register_ingredient_router

ingredients_routes = APIRouter(
    prefix="/ingredients",
    tags=["ingredients"],
    responses={404: {"description": "Not found"}},
)

ingredients_routes.include_router(register_ingredient_router)



