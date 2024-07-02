from sqlalchemy.orm import Session

from shared.utils.service_result import ServiceResult
from shared.utils.app_exceptions import AppExceptionCase
from modules.ingredients.schemas.domain import Ingredient
from models.ingredient import Ingredient as IngredientModel


class IngredientRepository():
    
    def __init__(self, db: Session):
        self.db = db

    async def register_ingredient(self, ingredient: Ingredient) -> ServiceResult:
        try:
            db_ingredient = IngredientModel(
                name=ingredient.name, 
                stock=ingredient.stock, 
                unit=ingredient.unit, 
                description=ingredient.description
            )

            self.db.add(db_ingredient)
            self.db.commit()
            self.db.refresh(db_ingredient)
            return ServiceResult("The ingredient have been registered!!")
        
        except Exception as e:
            print(f"An error occurred: {e}")
            self.db.rollback()
            return ServiceResult(AppExceptionCase(500, e))
