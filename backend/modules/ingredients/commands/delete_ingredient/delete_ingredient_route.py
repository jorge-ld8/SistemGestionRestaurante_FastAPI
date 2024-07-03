from fastapi import APIRouter, Depends
from starlette import status

from modules.ingredients.repositories.ingredient_repository import IngredientRepository
from modules.ingredients.commands.delete_ingredient.delete_ingredient_service import DeleteIngredientService
from shared.core.db.db_connection import get_db
from database import Session
from modules.users.user_auth.auth_decorators import authenticate_user, authorize_user
from modules.users.user_auth.auth_dependencies import get_current_user

from models import User

from shared.utils.service_result import handle_result

router = APIRouter()

def delete_ingredient_service():
    db: Session = next(get_db())
    repository = IngredientRepository(db)
    return DeleteIngredientService(repository)

@router.delete("/{ingredient_id}", status_code=status.HTTP_200_OK, name = "ingredients:delete_ingredient")
@authenticate_user()
@authorize_user(["admin"])
async def delete_ingredient(
    ingredient_id: int, 
    service: DeleteIngredientService = Depends(delete_ingredient_service),
    current_user: User = Depends(get_current_user)
):
    result = await service.delete_ingredient(ingredient_id)
    return handle_result(result)
