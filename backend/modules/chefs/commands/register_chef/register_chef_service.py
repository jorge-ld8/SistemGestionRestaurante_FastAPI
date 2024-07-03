from modules.chefs.schemas.dtos import RegisterChef
from modules.chefs.schemas.domain import Chef
from modules.chefs.repositories.chef_repository import ChefRepository
from shared.utils.app_exceptions import AppExceptionCase
from shared.utils.service_result import handle_result, ServiceResult


class RegisterChefService:
    
    def __init__(self, repository: ChefRepository):
        self.repository = repository
    
    async def register_chef(self, chef: RegisterChef) -> ServiceResult:
        try:
            new_chef = Chef(
                chef_id=0,
                name=chef.name,
                last_name=chef.last_name
            )

            saving_result = await self.repository.register_chef(new_chef)

            if not saving_result.success:
                handle_result(saving_result)
            
            return ServiceResult("The chef have been registered!!")
            
        except Exception as e:
            if hasattr(e, 'errors') and callable(e.errors):
                return ServiceResult(AppExceptionCase(400, e.errors()))
            
            return ServiceResult(AppExceptionCase(500, f"The next error have occurred: {e}"))
        