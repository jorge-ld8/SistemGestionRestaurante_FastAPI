from fastapi import APIRouter, Body, Depends
from starlette import status

from modules.ingredients.repositories.ingredient_repository import IngredientRepository
from modules.ingredients.schemas.dtos import RegisterIngredient
from modules.ingredients.commands.register_ingredient.register_ingredient_service import RegisterIngredientService
from shared.core.db.db_connection import get_db
from database import Session, Base
from modules.users.user_auth.auth_decorators import authenticate_user, authorize_user
from modules.users.user_auth.auth_dependencies import get_current_user

from models import User

from shared.utils.service_result import ServiceResult, handle_result

router = APIRouter()

def register_ingredient_service():
    db: Session = next(get_db())
    repository = IngredientRepository(db)
    return RegisterIngredientService(repository)

@router.post("/", status_code=status.HTTP_201_CREATED, name = "ingredients:register_ingredient")
@authenticate_user()
@authorize_user(["admin"])
async def register_ingredient(
    ingredient: RegisterIngredient = Body(..., embed=True), 
    service: RegisterIngredientService = Depends(register_ingredient_service),
    current_user: User = Depends(get_current_user)

):
    result = await service.register_ingredient(ingredient)
    return handle_result(result)