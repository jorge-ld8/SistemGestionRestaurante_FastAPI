from modules.chefs.repositories.chef_repository import ChefRepository
from shared.utils.app_exceptions import AppExceptionCase
from shared.utils.service_result import handle_result, ServiceResult


class DeleteChefService:

    def __init__(self, repository: ChefRepository):
        self.repository = repository

    async def delete_chef(self, chef_id: int) -> ServiceResult:
        try:
            saving_result = await self.repository.delete_chef(chef_id)

            if not saving_result.success:
                handle_result(saving_result)

            return ServiceResult("The chef has  been deleted!")

        except Exception as e:
            if hasattr(e, 'errors') and callable(e.errors):
                return ServiceResult(AppExceptionCase(400, e.errors()))

            return ServiceResult(AppExceptionCase(500, f"The next error have occurred: {e}"))
