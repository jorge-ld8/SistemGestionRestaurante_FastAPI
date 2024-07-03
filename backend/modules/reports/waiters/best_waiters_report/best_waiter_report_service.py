from shared.utils.service_result import ServiceResult, handle_result

from modules.orders.repositories.read_model.order_rm_repository import OrderReadModelRepository as OrderRepository
from shared.utils.app_exceptions import AppExceptionCase

class GetBestWaitersReportService:
        
    def __init__(self, orderRepository: OrderRepository):
        self.orderRepository = orderRepository

    async def get_best_waiters_report(self):
        try:

            waiters_search_result = await self.orderRepository.get_best_waiters_report()

            waiters = handle_result(waiters_search_result)

            if waiters is None:
                return ServiceResult(AppExceptionCase(404, "There are no waiters registered"))

            return ServiceResult(waiters)

        except Exception as e:
            if(hasattr(e, 'errors') and callable(e.errors)):
                return ServiceResult(AppExceptionCase(400, e.errors()))

            if(e.status_code):
                return ServiceResult(AppExceptionCase(e.status_code, e.msg))

            return ServiceResult(AppExceptionCase(500, f"The next error have ocurred: {e}"))
