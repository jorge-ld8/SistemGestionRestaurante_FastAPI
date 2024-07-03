from modules.orders.schemas.domain import Order
from shared.utils.app_exceptions import AppExceptionCase
from shared.utils.service_result import handle_result, ServiceResult
from modules.orders.repositories.order_repository import OrderRepository


class ChangeOrderStatusService:

    def __init__(self, order_repo: OrderRepository):
        self.order_repo = order_repo

    async def change_order_status(self, order_id: int, order_status: str) -> ServiceResult:
        try:
            order_result: Order = handle_result(await self.order_repo.get_order_by_id(order_id))

            if order_result is None:
                return ServiceResult("Order not found")

            new_order = Order(
                order_id=order_id,
                datetime=order_result.datetime,
                total=order_result.total,
                order_details=order_result.order_details,
                user_id=order_result.user_id,
                waiter_id=order_result.waiter_id,
                chef_id=order_result.chef_id,
                status=order_status)

            saving_result = await self.order_repo.update_order(new_order)

            if not saving_result.success:
                handle_result(saving_result)

            return ServiceResult(f'The order has been {order_status}!')

        except Exception as e:
            if hasattr(e, 'errors') and callable(e.errors):
                return ServiceResult(AppExceptionCase(400, e.errors()))
            return ServiceResult(AppExceptionCase(500, f"The next error have occurred: {e}"))



