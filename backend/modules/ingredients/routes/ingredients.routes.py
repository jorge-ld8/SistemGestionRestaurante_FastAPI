from fastapi import APIRouter, Body, Depends, Path, status

from modules.ingredients.schemas.dtos import RegisterIngredient
from modules.ingredients.services import RegisterIngredientService

router = APIRouter(
    responses={404: {"description": "Not found"}},
)

def register_ingredient_service():
    return RegisterIngredientService()

@router.post("/")
async def register_ingredient(ingredient: RegisterIngredient = Body(..., embed=True), service: RegisterIngredientService = Depends(register_ingredient_service)):
    
    pass