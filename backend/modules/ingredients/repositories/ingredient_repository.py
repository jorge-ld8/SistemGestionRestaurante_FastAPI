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
        
    async def get_ingredient_by_id(self, ingredient_id: int) -> ServiceResult:
        try:
            db_ingredient = self.db.query(IngredientModel).filter(
                (IngredientModel.ingredient_id == ingredient_id) &
                (IngredientModel.is_deleted == False)
                ).first()
            
            #Se devuelve None. No quiero lanzar exception aqui porque no es un error de la aplicacion. El bicho lit no existe
            if db_ingredient is None:
                return ServiceResult(None)
            
            ingredient = Ingredient(
                id=db_ingredient.ingredient_id,
                name=db_ingredient.name,
                stock=db_ingredient.stock,
                unit=db_ingredient.unit,
                description=db_ingredient.description
            )

            return ServiceResult(ingredient)
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return ServiceResult(AppExceptionCase(500, e))
        
    async def update_ingredient(self, ingredient: Ingredient) -> ServiceResult:
        try:
            db_ingredient = self.db.query(IngredientModel).filter(
                (IngredientModel.ingredient_id == ingredient.id) &
                (IngredientModel.is_deleted == False)
                ).first()

            if db_ingredient is None:
                return ServiceResult(AppExceptionCase(404, "The ingredient does not exist"))

            db_ingredient.name = ingredient.name
            db_ingredient.stock = ingredient.stock
            db_ingredient.unit = ingredient.unit
            db_ingredient.description = ingredient.description

            self.db.commit()
            self.db.refresh(db_ingredient)
            return ServiceResult("The ingredient have been updated!!")
        
        except Exception as e:
            print(f"An error occurred: {e}")
            self.db.rollback()
            return ServiceResult(AppExceptionCase(500, e))
        
