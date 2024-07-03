from sqlalchemy.orm import Session, joinedload, load_only
from typing import List

from shared.utils.service_result import ServiceResult
from shared.utils.app_exceptions import AppExceptionCase
from modules.menus.schemas.dtos import CheckPlateAvailability
from modules.menus.schemas.domain import Menu, PlateMenu
from modules.menus.schemas.domain import Plate
from models.menu import Menu as MenuModel
from models.plate_menu import PlatesMenu as PlateMenuModel
from models.plate import Plate as PlateModel
from models.plate_ingredient import PlateIngredient as PlateIngredientModel
from models.ingredient import Ingredient as IngredientModel

class MenuWriteModelRepository():

    def __init__(self, db: Session):
        self.db = db
    
    async def register_menu(self, menu: Menu) -> ServiceResult:
        try:
            db_menu = MenuModel(
                name=menu.name, 
                description=menu.description
            )

            self.db.add(db_menu)
            self.db.commit()
            self.db.refresh(db_menu)

            return ServiceResult("The menu have been registered!!")
        
        except Exception as e:
            print(f"An error occurred: {e}")
            self.db.rollback()
            return ServiceResult(AppExceptionCase(500, e))
    
    async def get_menu_basic_info(self, menu_id: int) -> ServiceResult:
        try:
            db_menu = self.db.query(MenuModel).filter(
                (MenuModel.menu_id == menu_id) &
                (MenuModel.is_deleted == False)
                ).first()
            
            if db_menu is None:
                return ServiceResult(None)
            
            menu = Menu(
                id=db_menu.menu_id,
                name=db_menu.name,
                description=db_menu.description
            )

            return ServiceResult(menu)
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return ServiceResult(AppExceptionCase(500, e))
    
    async def update_menu(self, menu: Menu) -> ServiceResult:
        try:
            db_menu = self.db.query(MenuModel).filter(
                (MenuModel.menu_id == menu.id) &
                (MenuModel.is_deleted == False)
                ).first()
            
            if db_menu is None:
                return ServiceResult(AppExceptionCase(404, "The menu does not exist"))
            
            db_menu.name = menu.name
            db_menu.description = menu.description

            self.db.commit()
            self.db.refresh(db_menu)
            return ServiceResult("The menu have been updated!!")
        
        except Exception as e:
            print(f"An error occurred: {e}")
            self.db.rollback()
            return ServiceResult(AppExceptionCase(500, e))
    
    async def delete_menu(self, menu_id: int) -> ServiceResult:
        try:
            db_menu = self.db.query(MenuModel).filter(
                (MenuModel.menu_id == menu_id) &
                (MenuModel.is_deleted == False)
                ).first()
            
            if db_menu is None:
                return ServiceResult(AppExceptionCase(404, "The menu does not exist"))
            
            db_menu.is_deleted = True

            self.db.commit()
            self.db.refresh(db_menu)
            return ServiceResult("The menu have been deleted!!")
        
        except Exception as e:
            print(f"An error occurred: {e}")
            self.db.rollback()
            return ServiceResult(AppExceptionCase(500, e))
    
    async def add_plate_to_menu(self, menu_id: int, plate_menu: PlateMenu) -> ServiceResult:
        try:
            db_plate_menu = PlateMenuModel(
                menu_id=menu_id,
                plate_id=plate_menu.plate.id,
                unit_price=plate_menu.unit_price
            )

            self.db.add(db_plate_menu)
            self.db.commit()
            self.db.refresh(db_plate_menu)

            return ServiceResult("The plate have been added to the menu!!")
        
        except Exception as e:
            print(f"An error occurred: {e}")
            self.db.rollback()
            return ServiceResult(AppExceptionCase(500, e))
    
    async def remove_plate_from_menu(self, menu_id: int, plate_id: int) -> ServiceResult:
        try:
            db_plate_menu = self.db.query(PlateMenuModel).filter(
                (PlateMenuModel.menu_id == menu_id) &
                (PlateMenuModel.plate_id == plate_id)
                ).first()
            
            if db_plate_menu is None:
                return ServiceResult(AppExceptionCase(404, "The plate does not exist in the menu"))
            
            self.db.delete(db_plate_menu)
            self.db.commit()

            return ServiceResult("The plate have been removed from the menu!!")
        
        except Exception as e:
            print(f"An error occurred: {e}")
            self.db.rollback()
            return ServiceResult(AppExceptionCase(500, e))
    
    async def update_plate_price_of_menu(self, plate_menu: PlateMenu):

        try:
            db_plate_menu = self.db.query(PlateMenuModel).filter(PlateMenuModel.plate_menu_id == plate_menu.id).first()

            if db_plate_menu is None:
                return ServiceResult(AppExceptionCase(404, "The plate does not exist in the menu"))
            
            db_plate_menu.unit_price = plate_menu.unit_price

            self.db.commit()
            self.db.refresh(db_plate_menu)

            return ServiceResult("The plate price have been updated in the menu!!")
            
        except Exception as e:
            print(f"An error occurred: {e}")
            self.db.rollback()
            return ServiceResult(AppExceptionCase(500, e))

    async def get_plate_menu_by_id(self, plate_menu_id: int) -> ServiceResult:
        try:
            db_plate_menu = (
            self.db.query(PlateMenuModel)
            .options(
                joinedload(PlateMenuModel.plate)
                .load_only(PlateModel.plate_id, PlateModel.name)
            )
            .filter(PlateMenuModel.plate_menu_id == plate_menu_id)
            .first()
            )
            
            if db_plate_menu is None:
                return ServiceResult(None)
            
            plate_menu = PlateMenu(
                id=db_plate_menu.plate_menu_id,
                plate = Plate(id=db_plate_menu.plate_id, name= db_plate_menu.plate.name),
                unit_price=db_plate_menu.unit_price
            )

            return ServiceResult(plate_menu)
        except Exception as e:
            print(f"An error occurred: {e}")
            return ServiceResult(AppExceptionCase(500, e))
        
    async def check_plates_availability(self, plates: List[CheckPlateAvailability]) -> ServiceResult:
        
        try:

            for plate in plates:
                plate_menu_id = plate.plate_menu_id

                db_plate_menu = (
                    self.db.query(PlateMenuModel)
                    .options(
                        joinedload(PlateMenuModel.plate)
                        .joinedload(PlateModel.ingredients)
                        .load_only(PlateIngredientModel.ingredient_id, PlateIngredientModel.quantity)
                    )
                    .filter(PlateMenuModel.plate_menu_id == plate_menu_id)
                    .one()
                )
                
                if db_plate_menu is None:
                    return ServiceResult(AppExceptionCase(404, f"The plate menu with id {plate_menu_id} does not exist"))

                ingredients = db_plate_menu.plate.ingredients

                if ingredients is None or len(ingredients) == 0:
                    return ServiceResult(AppExceptionCase(404, f"The plate menu with id {plate_menu_id} does not have ingredients"))

                for ingredient in ingredients:
                    db_ingredient = self.db.query(IngredientModel).filter(
                    (IngredientModel.ingredient_id == ingredient.ingredient_id) &
                    (IngredientModel.is_deleted == False)
                    ).first()

                    if db_ingredient is None:
                        return ServiceResult(AppExceptionCase(404, f"The ingredient with id {ingredient.ingredient_id} does not exist"))
                    
                    if db_ingredient.stock < ingredient.quantity * plate.quantity:
                        print(f"The ingredient {db_ingredient.name} with id {ingredient.ingredient_id} does not have enough stock. Needs {ingredient.quantity * plate.quantity} and has {db_ingredient.stock}")
                        return ServiceResult(False)

            
            return ServiceResult(True)
        except Exception as e:
            print(f"An error occurred: {e}")
            return ServiceResult(AppExceptionCase(500, e))