from shared.utils.service_result import ServiceResult, handle_result
from shared.utils.app_exceptions import AppExceptionCase
from modules.menus.schemas.domain import Menu
from modules.menus.repositories.write_model.menu_wm_repository import MenuWriteModelRepository as MenuRepository

class DeleteMenuService:
     def __init__(self, repository: MenuRepository):
        self.repository = repository
    
     async def delete_menu(self, menu_id: int) -> ServiceResult:
        try:
            
            delete_result = await self.repository.delete_menu(menu_id)

            handle_result(delete_result)
            
            return ServiceResult("The menu have been deleted!!")
        
        except Exception as e:
            if (e.status_code):
                return ServiceResult(AppExceptionCase(e.status_code, e.msg))
            
            return ServiceResult(AppExceptionCase(500, f"The next error have ocurred: {e}"));