from modules.waiters.repositories.waiter_repository import WaiterRepository
from shared.utils.app_exceptions import AppExceptionCase
from shared.utils.service_result import handle_result, ServiceResult


class GetWaiterService:

    def __init__(self, repository: WaiterRepository):
        self.repository = repository

    async def get_waiter_by_id(self, waiter_id: int) -> ServiceResult:
        try:
            waiter_result = handle_result(await self.repository.get_waiter_by_id(waiter_id))

            if waiter_result is None:
                return ServiceResult("Waiter not found")

            return ServiceResult(waiter_result)

        except Exception as e:
            if hasattr(e, 'errors') and callable(e.errors):
                return ServiceResult(AppExceptionCase(400, e.errors()))

            return ServiceResult(AppExceptionCase(500, f"The next error has occurred: {e}"))
