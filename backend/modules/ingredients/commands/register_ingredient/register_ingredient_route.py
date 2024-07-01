from fastapi import APIRouter, Body, Depends

from modules.ingredients.schemas.dtos import RegisterIngredient
from modules.ingredients.commands.register_ingredient.register_ingredient_service import RegisterIngredientService
from shared.utils.service_result import ServiceResult, handle_result

router = APIRouter()

def register_ingredient_service():
    return RegisterIngredientService()

@router.post("/")
async def register_ingredient(ingredient: RegisterIngredient = Body(..., embed=True), service: RegisterIngredientService = Depends(register_ingredient_service)):
    result = await service.register_ingredient(ingredient)
    return handle_result(result)