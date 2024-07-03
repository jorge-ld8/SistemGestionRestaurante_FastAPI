from sqlalchemy.orm import Session

from shared.utils.service_result import ServiceResult, handle_result
from shared.utils.app_exceptions import AppExceptionCase
from models.ingredient import Ingredient as IngredientModel

class IngredientReadModelRepository:

    def __init__(self, db: Session):
        self.db = db
    
    async def get_ingredients_report(self) -> ServiceResult:
        try:
            ingredients = self.db.query(IngredientModel).filter(IngredientModel.is_deleted == False).all()
            return ServiceResult(ingredients)
        except Exception as e:
            print(f"An error occurred: {e}")
            return ServiceResult(AppExceptionCase(500, e))