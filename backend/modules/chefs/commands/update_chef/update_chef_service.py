from modules.chefs.schemas.dtos import UpdateChef
from modules.chefs.schemas.domain import Chef
from modules.chefs.repositories.chef_repository import ChefRepository
from shared.utils.app_exceptions import AppExceptionCase
from shared.utils.service_result import handle_result, ServiceResult


class UpdateChefService:

    def __init__(self, repository: ChefRepository):
        self.repository = repository

    async def update_chef(self, chef: UpdateChef, chef_id: int) -> ServiceResult:
        try:
            chef_result: Chef = handle_result(await self.repository.get_chef_by_id(chef_id))

            if chef_result is None:
                return ServiceResult("Chef not found")

            new_chef = Chef(
                chef_id=chef_id,
                name=chef.name if chef.name is not None else chef_result.name,
                last_name=chef.last_name if chef.last_name is not None else chef_result.last_name,
            )

            saving_result = await self.repository.update_chef(new_chef)

            if not saving_result.success:
                handle_result(saving_result)

            return ServiceResult("The chef has been updated")

        except Exception as e:
            if hasattr(e, 'errors') and callable(e.errors):
                return ServiceResult(AppExceptionCase(400, e.errors()))

            return ServiceResult(AppExceptionCase(500, f"The next error have occurred: {e}"))
