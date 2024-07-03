from fastapi import APIRouter, Depends
from starlette import status

from modules.ingredients.repositories.read_model.ingredient_rm_repository import IngredientReadModelRepository as IngredientRepository
from modules.reports.ingredients.ingredients_report.get_ingredients_report_service import GetIngredientsReportService
from shared.core.db.db_connection import get_db
from database import Session

from shared.utils.service_result import handle_result

router = APIRouter()

def get_ingredients_report_service():
    db: Session = next(get_db())
    ingredient_repository = IngredientRepository(db)
    return GetIngredientsReportService(ingredient_repository)