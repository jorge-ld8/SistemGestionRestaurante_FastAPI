from fastapi import APIRouter, Depends
from starlette import status

from modules.ingredients.repositories.ingredient_repository import IngredientRepository
from modules.ingredients.commands.delete_ingredient.delete_ingredient_service import DeleteIngredientService
from shared.core.db.db_connection import get_db
from database import Session

from shared.utils.service_result import handle_result

router = APIRouter()

def delete_ingredient_service():
    db: Session = next(get_db())
    repository = IngredientRepository(db)
    return DeleteIngredientService(repository)

@router.delete("/{ingredient_id}", status_code=status.HTTP_200_OK, name = "ingredients:delete_ingredient")
async def delete_ingredient(
    ingredient_id: int, 
    service: DeleteIngredientService = Depends(delete_ingredient_service)
):
    result = await service.delete_ingredient(ingredient_id)
    return handle_result(result)
