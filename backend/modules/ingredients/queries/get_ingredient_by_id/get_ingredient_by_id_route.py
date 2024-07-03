from fastapi import APIRouter, Depends
from starlette import status

from modules.ingredients.repositories.ingredient_repository import IngredientRepository
from modules.ingredients.schemas.dtos import UpdateIngredient
from modules.ingredients.queries.get_ingredient_by_id.get_ingredient_by_id_service import GetIngredientByIdService
from shared.core.db.db_connection import get_db
from database import Session, Base
from modules.users.user_auth.auth_decorators import authenticate_user, authorize_user
from modules.users.user_auth.auth_dependencies import get_current_user

from models import User
from shared.utils.service_result import ServiceResult, handle_result

router = APIRouter()

def get_ingrediente_service():
    db: Session = next(get_db())
    repository = IngredientRepository(db)
    return GetIngredientByIdService(repository)

@router.get("/{ingredient_id}", status_code=status.HTTP_200_OK, name = "ingredients:get_ingredient_by_id")
@authenticate_user()
@authorize_user(["admin"])
async def get_ingredient_by_id(
    ingredient_id: int, 
    service: GetIngredientByIdService = Depends(get_ingrediente_service),
    current_user: User = Depends(get_current_user)
):
    result = await service.get_ingredient_by_id(ingredient_id)
    return handle_result(result)