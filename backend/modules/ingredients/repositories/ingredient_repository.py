from sqlalchemy.orm import Session

from shared.utils.service_result import ServiceResult, handle_result
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
            db_ingredient.unit = ingredient.unit
            db_ingredient.description = ingredient.description

            self.db.commit()
            self.db.refresh(db_ingredient)
            return ServiceResult("The ingredient have been updated!!")
        
        except Exception as e:
            print(f"An error occurred: {e}")
            self.db.rollback()
            return ServiceResult(AppExceptionCase(500, e))
        
    async def delete_ingredient(self, ingredient_id: int):
        try:
            db_ingredient = self.db.query(IngredientModel).filter(
                (IngredientModel.ingredient_id == ingredient_id) &
                (IngredientModel.is_deleted == False)
                ).first()

            if db_ingredient is None:
                return ServiceResult(AppExceptionCase(404, "The ingredient does not exist"))
                
            db_ingredient.is_deleted = True
            self.db.commit()
            self.db.refresh(db_ingredient)
            return ServiceResult("The ingredient have been deleted!!")
        
        except Exception as e:
            print(f"An error occurred: {e}")
            self.db.rollback()
            return ServiceResult(AppExceptionCase(500, e))
    
    async def adjust_ingredient_stock(self, ingredient: Ingredient) -> ServiceResult:
        try:
            db_ingredient = self.db.query(IngredientModel).filter(
                (IngredientModel.ingredient_id == ingredient.id) &
                (IngredientModel.is_deleted == False)
                ).first()

            if db_ingredient is None:
                return ServiceResult(AppExceptionCase(404, "The ingredient does not exist"))

            db_ingredient.stock = ingredient.stock

            self.db.commit()
            self.db.refresh(db_ingredient)
            return ServiceResult("The ingredient stock have  been adjusted!!")
        
        except Exception as e:
            print(f"An error occurred: {e}")
            self.db.rollback()
            return ServiceResult(AppExceptionCase(500, e))
    
    async def get_ingredients_by_ids(self, ingredientsIds: list[int]) -> ServiceResult:
        try:

            ingredients = []

            for ingredient_id in ingredientsIds:
                db_ingredient_result = await self.get_ingredient_by_id(ingredient_id)
                db_ingredient = handle_result(db_ingredient_result)

                if db_ingredient is None:
                    return ServiceResult(AppExceptionCase(404, f"The ingredient with id {ingredient_id} does not exist"))

                ingredient = Ingredient(
                    id=db_ingredient.id,
                    name=db_ingredient.name,
                    stock=db_ingredient.stock,
                    unit=db_ingredient.unit,
                    description=db_ingredient.description
                )

                ingredients.append(ingredient)
           
            return ServiceResult(ingredients)
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return ServiceResult(AppExceptionCase(500, e))