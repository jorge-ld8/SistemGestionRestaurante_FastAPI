from fastapi import APIRouter, Body, Depends
from starlette import status

from modules.ingredients.repositories.ingredient_repository import IngredientRepository
from modules.ingredients.schemas.dtos import UpdateIngredient
from modules.ingredients.commands.update_ingredient.update_ingredient_service import UpdateIngredientService
from shared.core.db.db_connection import get_db
from database import Session

from shared.utils.service_result import handle_result

router = APIRouter()

def update_ingredient_service():
    db: Session = next(get_db())
    repository = IngredientRepository(db)
    return UpdateIngredientService(repository)

@router.put("/{ingredient_id}", status_code=status.HTTP_200_OK, name = "ingredients:update_ingredient")
async def update_ingredient(
    ingredient_id: int, 
    ingredient: UpdateIngredient = Body(..., embed=True), 
    service: UpdateIngredientService = Depends(update_ingredient_service)
):
    result = await service.update_ingredient(ingredient_id, ingredient)
    return handle_result(result)