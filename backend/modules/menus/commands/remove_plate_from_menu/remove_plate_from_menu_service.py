from shared.utils.service_result import ServiceResult, handle_result
from shared.utils.app_exceptions import AppExceptionCase
from modules.menus.repositories.write_model.menu_wm_repository import MenuWriteModelRepository as MenuRepository

class RemovePlateFromMenuService:
        
        def __init__(self, menu_repository: MenuRepository):
            self.menu_repository = menu_repository
        
        async def remove_plate_from_menu(self, menu_id:int, plate_id:int) -> ServiceResult:
            try:
    
                savingResult = await self.menu_repository.remove_plate_from_menu(menu_id, plate_id)
    
                if not savingResult.success:
                    handle_result(savingResult)
                
                
                return ServiceResult("The plate have been removed from the menu!!")
                
            except Exception as e:
                if(hasattr(e, 'errors') and callable(e.errors)):
                    return ServiceResult(AppExceptionCase(400, e.errors()))

                if (e.status_code):
                    return ServiceResult(AppExceptionCase(e.status_code, e.msg))
                
                return ServiceResult(AppExceptionCase(500, f"The next error have ocurred: {e}"))