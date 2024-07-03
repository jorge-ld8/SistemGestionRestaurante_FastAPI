from sqlalchemy.orm import Session

from shared.utils.service_result import ServiceResult
from shared.utils.app_exceptions import AppExceptionCase
from modules.plates.schemas.domain import Plate, PlateIngredient
from models.plate import Plate as PlateModel
from models.plate_ingredient import PlateIngredient as PlateIngredientModel

class PlateWriteModelRepository():
    def __init__(self, db: Session):
        self.db = db
    
    async def register_plate(self, plate: Plate) -> ServiceResult:
        try:
            db_plate = PlateModel(
                name = plate.name,
                description = plate.description
            )

            self.db.add(db_plate)
            self.db.commit()  

            for ingredient in plate.ingredients:
                db_plate_ingredient = PlateIngredientModel(
                    plate_id = db_plate.plate_id,
                    ingredient_id = ingredient.ingredient.id,
                    quantity = ingredient.quantity
                )
                self.db.add(db_plate_ingredient)
            
            self.db.commit()
            self.db.refresh(db_plate)

            return ServiceResult("The plate have been registered!!")
        
        except Exception as e:
            print(f"An error occurred: {e}")
            self.db.rollback()
            return ServiceResult(AppExceptionCase(500, e))
    
    async def get_plate_basic_info_by_id(self, plate_id: int) -> ServiceResult:
        try:
            db_plate = self.db.query(PlateModel).filter(
                (PlateModel.plate_id == plate_id) &
                (PlateModel.is_deleted == False)
            ).first()

            if db_plate is None:
                return ServiceResult(None)

            plate = Plate(
                id = db_plate.plate_id,
                name = db_plate.name,
                description = db_plate.description,
                ingredients = []
            )

            return ServiceResult(plate)
        except Exception as e:
            print(f"An error occurred: {e}")
            return ServiceResult(AppExceptionCase(500, e))
    
    async def get_plate_ingredients_by_plate_id(self, plate_id: int) -> ServiceResult:
        try:
            db_plate_ingredients = self.db.query(PlateIngredientModel).filter(
                (PlateIngredientModel.plate_id == plate_id)
            ).all()

            if db_plate_ingredients is None:
                return ServiceResult(None)
            
            return ServiceResult(db_plate_ingredients)
            
        except Exception as e:
            print(f"An error occurred: {e}")
            return ServiceResult(AppExceptionCase(500, e))
    
    async def update_plate(self, plate: Plate) -> ServiceResult:
        try:
            db_plate = self.db.query(PlateModel).filter(
                (PlateModel.plate_id == plate.id) &
                (PlateModel.is_deleted == False)
            ).first()

            if db_plate is None:
                return ServiceResult(AppExceptionCase(404, "The plate does not exist"))

            db_plate.name = plate.name
            db_plate.description = plate.description

            self.db.commit()
            self.db.refresh(db_plate)

            return ServiceResult("The plate have been updated!!")
        except Exception as e:
            print(f"An error occurred: {e}")
            self.db.rollback()
            return ServiceResult(AppExceptionCase(500, e))
    
    async def delete_plate(self, plate_id: int) -> ServiceResult:
        try:
            db_plate = self.db.query(PlateModel).filter(
                (PlateModel.plate_id == plate_id) &
                (PlateModel.is_deleted == False)
            ).first()

            if db_plate is None:
                return ServiceResult(AppExceptionCase(404, "The plate does not exist"))
            
            db_plate.is_deleted = True
            self.db.commit()
            self.db.refresh(db_plate)

            return ServiceResult("The plate have been deleted!!")
        except Exception as e:
            print(f"An error occurred: {e}")
            self.db.rollback()
            return ServiceResult(AppExceptionCase(500, e))

    async def get_plate_ingredient(self, plate_id: int, ingredient_id: int) -> ServiceResult:
        try:
            db_plate_ingredient = self.db.query(PlateIngredientModel).filter(
                (PlateIngredientModel.plate_id == plate_id) &
                (PlateIngredientModel.ingredient_id == ingredient_id)
            ).first()

            if db_plate_ingredient is None:
                return ServiceResult(None)
        
            return ServiceResult(db_plate_ingredient)
            
        except Exception as e:
            print(f"An error occurred: {e}")
            return ServiceResult(AppExceptionCase(500, e))

    async def adjust_ingredient_quantity(self, plate_id: int, plate_ingredient: PlateIngredient) -> ServiceResult:
        try:
            db_plate_ingredient = self.db.query(PlateIngredientModel).filter(
                (PlateIngredientModel.plate_id == plate_id) &
                (PlateIngredientModel.ingredient_id == plate_ingredient.ingredient.id)
            ).first()

            if db_plate_ingredient is None:
                return ServiceResult("That plate with that ingredient does not exist")
            
            db_plate_ingredient.quantity = plate_ingredient.quantity

            self.db.commit()
            self.db.refresh(db_plate_ingredient)

            return ServiceResult("The ingredient quantity have been adjusted!!")
            
        except Exception as e:
            print(f"An error occurred: {e}")
            return ServiceResult(AppExceptionCase(500, e))
