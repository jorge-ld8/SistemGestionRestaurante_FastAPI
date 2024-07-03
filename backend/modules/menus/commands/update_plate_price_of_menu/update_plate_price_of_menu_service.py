from shared.utils.service_result import ServiceResult, handle_result
from shared.utils.app_exceptions import AppExceptionCase
from modules.menus.schemas.domain import PlateMenu
from modules.menus.schemas.dtos import UpdatePlatePriceOfMenu
from modules.menus.repositories.write_model.menu_wm_repository import MenuWriteModelRepository as MenuRepository

class UpdatePlatePriceOfMenuService:
            
            def __init__(self, menu_repository: MenuRepository):
                self.menu_repository = menu_repository
            
            async def update_plate_price_of_menu(self, plate_menu_id: int, dto: UpdatePlatePriceOfMenu) -> ServiceResult:
                try:

                    plate_menu_search_result = await self.menu_repository.get_plate_menu_by_id(plate_menu_id)

                    old_plate_menu = handle_result(plate_menu_search_result)

                    if old_plate_menu is None:
                        return ServiceResult(AppExceptionCase(404, "The plate menu does not exist"))
                    
                    plate_menu_updated= PlateMenu(
                        id=old_plate_menu.id,
                        plate=old_plate_menu.plate,
                        unit_price=dto.unit_price,
                    )
                    
                    savingResult = await self.menu_repository.update_plate_price_of_menu(plate_menu_updated)
                    
                    if not savingResult.success:
                        handle_result(savingResult)
                    
                    return ServiceResult("The plate price have been updated on the menu!!")
                
                except Exception as e:
                    if(hasattr(e, 'errors') and callable(e.errors)):
                        return ServiceResult(AppExceptionCase(400, e.errors()))
                    
                    if(e.status_code):
                        return ServiceResult(AppExceptionCase(e.status_code, e.msg))
                    
                    return ServiceResult(AppExceptionCase(500, f"The next error have ocurred: {e}"))