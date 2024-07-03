from modules.waiters.repositories.waiter_repository import WaiterRepository
from shared.utils.app_exceptions import AppExceptionCase
from shared.utils.service_result import handle_result, ServiceResult


class DeleteWaiterService:

    def __init__(self, repository: WaiterRepository):
        self.repository = repository

    async def delete_waiter(self, waiter_id: int) -> ServiceResult:
        try:
            saving_result = await self.repository.delete_waiter(waiter_id)

            if not saving_result.success:
                handle_result(saving_result)

            return ServiceResult("The waiter has  been deleted!")

        except Exception as e:
            if hasattr(e, 'errors') and callable(e.errors):
                return ServiceResult(AppExceptionCase(400, e.errors()))
            
            if(e.status_code):
                return ServiceResult(AppExceptionCase(e.status_code, e.msg))

            return ServiceResult(AppExceptionCase(500, f"The next error have occurred: {e}"))
