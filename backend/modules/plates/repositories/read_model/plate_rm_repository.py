from sqlalchemy.orm import Session, joinedload, load_only

from shared.utils.service_result import ServiceResult
from shared.utils.app_exceptions import AppExceptionCase
from models.plate import Plate as PlateModel
from models.plate_ingredient import PlateIngredient as PlateIngredientModel
from models.ingredient import Ingredient as IngredientModel
 
class PlateReadModelRepository():
    def __init__(self, db: Session):
        self.db = db
    
    async def get_plate_by_id(self, plate_id:int) -> ServiceResult:
        try:
            plate = (
                self.db.query(PlateModel)
                .options(load_only(PlateModel.plate_id, PlateModel.name, PlateModel.description),
                joinedload(PlateModel.ingredients)
                .load_only(PlateIngredientModel.quantity)
                .joinedload(PlateIngredientModel.ingredient)
                .load_only(IngredientModel.ingredient_id, IngredientModel.name, IngredientModel.description)
                )
                .filter(PlateModel.plate_id == plate_id, PlateModel.is_deleted == False)
                .first()
            )

            return ServiceResult(plate)
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return ServiceResult(AppExceptionCase(500, e))