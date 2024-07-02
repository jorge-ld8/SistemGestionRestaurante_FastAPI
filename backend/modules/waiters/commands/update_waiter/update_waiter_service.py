from modules.waiters.schemas.dtos import UpdateWaiter
from modules.waiters.schemas.domain import Waiter
from modules.waiters.repositories.waiter_repository import WaiterRepository
from shared.utils.app_exceptions import AppExceptionCase
from shared.utils.service_result import handle_result, ServiceResult


class UpdateWaiterService:

    def __init__(self, repository: WaiterRepository):
        self.repository = repository

    async def update_waiter(self, waiter: UpdateWaiter, waiter_id: int) -> ServiceResult:
        try:
            waiter_result: Waiter = handle_result(await self.repository.get_waiter_by_id(waiter_id))

            if waiter_result is None:
                return ServiceResult("Waiter not found")

            new_waiter = Waiter(
                waiter_id=waiter_id,
                name=waiter.name if waiter.name is not None else waiter_result.name,
                last_name=waiter.last_name if waiter.last_name is not None else waiter_result.last_name,
            )

            saving_result = await self.repository.update_waiter(new_waiter)

            if not saving_result.success:
                handle_result(saving_result)

            return ServiceResult("The waiter has been updated")

        except Exception as e:
            if hasattr(e, 'errors') and callable(e.errors):
                return ServiceResult(AppExceptionCase(400, e.errors()))

            return ServiceResult(AppExceptionCase(500, f"The next error have occurred: {e}"))
