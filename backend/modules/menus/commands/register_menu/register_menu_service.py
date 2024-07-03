
from shared.utils.service_result import ServiceResult, handle_result
from shared.utils.app_exceptions import AppExceptionCase
from modules.menus.schemas.domain import Menu
from modules.menus.schemas.dtos import RegisterMenu, CheckPlateAvailability
from modules.menus.repositories.write_model.menu_wm_repository import MenuWriteModelRepository as MenuRepository

class RegisterMenuService:
    
    def __init__(self, repository: MenuRepository):
        self.repository = repository
    
    async def register_menu(self, dto: RegisterMenu) -> ServiceResult:
        try:

            newMenu = Menu(
                id=0,
                name=dto.name,
                description=dto.description
            )

            savingResult = await self.repository.register_menu(newMenu)

            if not savingResult.success:
                handle_result(savingResult)
            
            return ServiceResult("The menu have been registered!!")
        
            
        except Exception as e:
            if(hasattr(e, 'errors') and callable(e.errors)):
                return ServiceResult(AppExceptionCase(400, e.errors()))
            
            return ServiceResult(AppExceptionCase(500, f"The next error have ocurred: {e}"))
