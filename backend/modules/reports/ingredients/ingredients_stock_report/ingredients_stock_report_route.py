from fastapi import APIRouter, Depends
from starlette import status

from modules.ingredients.repositories.read_model.ingredient_rm_repository import IngredientReadModelRepository as IngredientRepository
from modules.reports.ingredients.ingredients_stock_report.ingredients_stock_report_service import GetIngredientsReportService
from shared.core.db.db_connection import get_db
from database import Session
from modules.users.user_auth.auth_decorators import authenticate_user, authorize_user
from modules.users.user_auth.auth_dependencies import get_current_user

from models import User

from shared.utils.service_result import handle_result

router = APIRouter()

def get_ingredients_report_service():
    db: Session = next(get_db())
    ingredient_repository = IngredientRepository(db)
    return GetIngredientsReportService(ingredient_repository)

@router.get("/ingredients-stock-report", status_code=status.HTTP_200_OK, name="Reports:Get Ingredients Stock Report")
@authenticate_user()
@authorize_user(["admin"])
async def get_ingredients_report(
    service: GetIngredientsReportService = Depends(get_ingredients_report_service), 
    current_user: User = Depends(get_current_user)
):
    result = await service.get_ingredients_report()
    return handle_result(result)