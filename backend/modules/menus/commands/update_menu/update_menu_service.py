from shared.utils.service_result import ServiceResult, handle_result
from shared.utils.app_exceptions import AppExceptionCase
from modules.menus.schemas.domain import Menu
from modules.menus.schemas.dtos import UpdateMenu
from modules.menus.repositories.write_model.menu_wm_repository import MenuWriteModelRepository as MenuRepository

class UpdateMenuService:
        
        def __init__(self, repository: MenuRepository):
            self.repository = repository
        
        async def update_menu(self, menu_id: int, dto: UpdateMenu) -> ServiceResult:
            try:
                
                menu_search_result = await self.repository.get_menu_basic_info(menu_id)

                menu = handle_result(menu_search_result)

                if not menu:
                    return ServiceResult(AppExceptionCase(404, "The menu does not exist"))
                
                menu_updated = Menu(
                    id=menu_id,
                    name=dto.name if dto.name else menu.name,
                    description=dto.description if dto.description else menu.description
                )
    
                savingResult = await self.repository.update_menu(menu_updated)
    
                if not savingResult.success:
                    handle_result(savingResult)
                
                
                return ServiceResult("The menu have been updated!!")
                
            except Exception as e:
                if(hasattr(e, 'errors') and callable(e.errors)):
                    return ServiceResult(AppExceptionCase(400, e.errors()))
                
                return ServiceResult(AppExceptionCase(500, f"The next error have ocurred: {e}"))


