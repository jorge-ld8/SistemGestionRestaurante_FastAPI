from shared.utils.service_result import ServiceResult, handle_result
from shared.utils.app_exceptions import AppExceptionCase
from modules.menus.schemas.domain import PlateMenu
from modules.menus.schemas.dtos import AddPlateToMenu
from modules.menus.repositories.write_model.menu_wm_repository import MenuWriteModelRepository as MenuRepository
from modules.plates.repositories.write_model.plate_wm_repository import PlateWriteModelRepository as PlateRepository

class AddPlateToMenuService:
        
        def __init__(self, menu_repository: MenuRepository, plate_repository: PlateRepository):
            self.menu_repository = menu_repository
            self.plate_repository = plate_repository
        
        async def add_plate_to_menu(self, menu_id:int, dto: AddPlateToMenu) -> ServiceResult:
            try:
                plate_search_result = await self.plate_repository.get_plate_basic_info_by_id(dto.plate_id)
                
                plate = handle_result(plate_search_result)

                if plate is None:
                    return ServiceResult(AppExceptionCase(404, "The plate does not exist"))
                
                plate_menu = PlateMenu(
                     id=0,
                    plate=plate,
                    unit_price=dto.unit_price,
                )
                
                savingResult = await self.menu_repository.add_plate_to_menu(menu_id, plate_menu)
                
                if not savingResult.success:
                    handle_result(savingResult)
                
                return ServiceResult("The plate have been added to the menu!!")
            
            except Exception as e:
                if(hasattr(e, 'errors') and callable(e.errors)):
                    return ServiceResult(AppExceptionCase(400, e.errors()))
                
                return ServiceResult(AppExceptionCase(500, f"The next error have ocurred: {e}"))
