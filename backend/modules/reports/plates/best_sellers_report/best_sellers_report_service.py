from shared.utils.service_result import ServiceResult, handle_result

from modules.orders.repositories.read_model.order_rm_repository import OrderReadModelRepository as OrderRepository
from shared.utils.app_exceptions import AppExceptionCase

class BestSellersReportService:
            
    def __init__(self, orderRepository: OrderRepository):
        self.orderRepository = orderRepository

    async def get_best_sellers_report(self):
        try:

            best_sellers_search_result = await self.orderRepository.get_best_sellers_report()

            best_sellers = handle_result(best_sellers_search_result)

            if best_sellers is None:
                return ServiceResult(AppExceptionCase(404, "There are no best sellers registered"))

            return ServiceResult(best_sellers)

        except Exception as e:
            if(hasattr(e, 'errors') and callable(e.errors)):
                return ServiceResult(AppExceptionCase(400, e.errors()))

            if(e.status_code):
                return ServiceResult(AppExceptionCase(e.status_code, e.msg))

            return ServiceResult(AppExceptionCase(500, f"The next error have ocurred: {e}"))