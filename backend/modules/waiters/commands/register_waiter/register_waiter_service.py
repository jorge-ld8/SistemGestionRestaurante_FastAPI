from modules.waiters.schemas.dtos import RegisterWaiter
from modules.waiters.schemas.domain import Waiter
from modules.waiters.repositories.waiter_repository import WaiterRepository
from shared.utils.app_exceptions import AppExceptionCase
from shared.utils.service_result import handle_result, ServiceResult


class RegisterWaiterService:
    
    def __init__(self, repository: WaiterRepository):
        self.repository = repository
    
    async def register_waiter(self, waiter: RegisterWaiter) -> ServiceResult:
        try:
            new_waiter = Waiter(
                waiter_id=0,
                name=waiter.name,
                last_name=waiter.last_name
            )

            saving_result = await self.repository.register_waiter(new_waiter)

            if not saving_result.success:
                handle_result(saving_result)
            
            return ServiceResult("The waiter have been registered!!")
            
        except Exception as e:
            if hasattr(e, 'errors') and callable(e.errors):
                return ServiceResult(AppExceptionCase(400, e.errors()))
            
            return ServiceResult(AppExceptionCase(500, f"The next error have occurred: {e}"))
        