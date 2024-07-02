from sqlalchemy.orm import Session

from shared.utils.service_result import ServiceResult
from shared.utils.app_exceptions import AppExceptionCase
from modules.menus.schemas.domain import Menu, PlateMenu
from models.menu import Menu as MenuModel
from models.plate_menu import PlatesMenu as PlateMenuModel

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