from sqlalchemy.orm import Session, joinedload, load_only

from shared.utils.service_result import ServiceResult
from shared.utils.app_exceptions import AppExceptionCase
from models.menu import Menu as MenuModel
from models.plate_menu import PlatesMenu as PlateMenuModel
from models.plate import Plate as PlateModel
from models.plate_ingredient import PlateIngredient as PlateIngredientModel
from models.ingredient import Ingredient as IngredientModel

class MenuReadModelRepository():

    def __init__(self, db: Session):
        self.db = db
    
    async def get_menu_by_id(self, menu_id: int) -> ServiceResult:
        try:
            menu = (
                self.db.query(MenuModel)
                .options(load_only(MenuModel.menu_id, MenuModel.name, MenuModel.description),
                    joinedload(MenuModel.plates)
                    .load_only(PlateMenuModel.unit_price)
                    .joinedload(PlateMenuModel.plate)
                    .load_only(PlateModel.plate_id, PlateModel.name, PlateModel.description)
                    .joinedload(PlateModel.ingredients)
                    .load_only(PlateIngredientModel.quantity)
                    .joinedload(PlateIngredientModel.ingredient)
                    .load_only(IngredientModel.ingredient_id, IngredientModel.name, IngredientModel.description)
                )
                .filter(MenuModel.menu_id == menu_id, MenuModel.is_deleted == False)
                .one()
            )

            return ServiceResult(menu)

        except Exception as e:
            print(f"An error occurred: {e}")
            return ServiceResult(AppExceptionCase(500, e))
    
