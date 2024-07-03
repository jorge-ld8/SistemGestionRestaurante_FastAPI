from shared.utils.service_result import ServiceResult, handle_result
from shared.utils.app_exceptions import AppExceptionCase
from modules.menus.repositories.read_model.menu_rm_repository import MenuReadModelRepository as MenuRepository

class GetMenuByIdService:
    
    def __init__(self, repository: MenuRepository):
        self.repository = repository
    
    async def get_menu_by_id(self, menu_id: int) -> ServiceResult:
        try:
            
            menu_search_result = await self.repository.get_menu_by_id(menu_id)
           
            menu = handle_result(menu_search_result)
            
            if menu is None:
                return ServiceResult(AppExceptionCase(404, "The menu does not exist"))
            
            return ServiceResult(menu)
        
        except Exception as e:
            if(hasattr(e, 'errors') and callable(e.errors)):
                return ServiceResult(AppExceptionCase(400, e.errors()))
            
            if(e.status_code):
                return ServiceResult(AppExceptionCase(e.status_code, e.msg))
            
            return ServiceResult(AppExceptionCase(500, f"The next error have ocurred: {e}"))
