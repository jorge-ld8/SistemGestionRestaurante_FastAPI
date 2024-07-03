from modules.chefs.repositories.chef_repository import ChefRepository
from shared.utils.app_exceptions import AppExceptionCase
from shared.utils.service_result import handle_result, ServiceResult


class GetChefService:

    def __init__(self, repository: ChefRepository):
        self.repository = repository

    async def get_chef_by_id(self, chef_id: int) -> ServiceResult:
        try:
            chef_result = await self.repository.get_chef_by_id(chef_id)

            if handle_result(chef_result) is None:
                return ServiceResult("Chef not found")

            return ServiceResult(chef_result)

        except Exception as e:
            if hasattr(e, 'errors') and callable(e.errors):
                return ServiceResult(AppExceptionCase(400, e.errors()))

            return ServiceResult(AppExceptionCase(500, f"The next error has occurred: {e}"))
