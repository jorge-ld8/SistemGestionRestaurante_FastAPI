from fastapi import APIRouter, Body, Depends
from starlette import status

from modules.ingredients.repositories.ingredient_repository import IngredientRepository
from modules.ingredients.schemas.dtos import AdjustIngredientStock
from modules.ingredients.commands.adjust_ingredient_stock.adjust_ingredient_stock_service import AdjustIngredientStockService
from shared.core.db.db_connection import get_db
from database import Session
from modules.users.user_auth.auth_decorators import authenticate_user, authorize_user
from modules.users.user_auth.auth_dependencies import get_current_user

from models import User

from shared.utils.service_result import handle_result

router = APIRouter()

def adjust_ingredient_stock_service():
    db: Session = next(get_db())
    repository = IngredientRepository(db)
    return AdjustIngredientStockService(repository)

@router.put("/{ingredient_id}/stock", status_code=status.HTTP_201_CREATED, name = "ingredients:adjust_ingredient_stock")
@authenticate_user()
@authorize_user(["admin"])
async def adjust_ingredient_stock(
    ingredient_id: int, 
    ingredient: AdjustIngredientStock = Body(..., embed=True), 
    service: AdjustIngredientStockService = Depends(adjust_ingredient_stock_service),
    current_user = Depends(get_current_user)
):
    result = await service.adjust_ingredient_stock(ingredient_id, ingredient)
    return handle_result(result)