from backend.modules.orders.schemas.domain import Order
from backend.shared.utils.app_exceptions import AppExceptionCase
from backend.modules.orders.repositories.order_repository import OrderRepository
from backend.modules.orders.schemas.dtos import RegisterOrder
from backend.shared.utils.service_result import handle_result, ServiceResult


class RegisterOrderService:

    def __init__(self, repository: OrderRepository):
        self.repository = repository

    async def register_order(self, order: RegisterOrder) -> ServiceResult:
        try:
            # save order details


            # calculate total
            total_order = 100

            # Generate Order domain object
            new_order = Order(
                plates=order.plates,
                user_id=order.user_id,
                chef_id=order.chef_id,
                waiter_id=order.waiter_id,
                total=total_order
            )

            saving_result = await self.repository.register_order(new_order)

            if not saving_result.success:
                handle_result(saving_result)

            return ServiceResult("The order have been registered!!")

        except Exception as e:
            if hasattr(e, 'errors') and callable(e.errors):
                return ServiceResult(AppExceptionCase(400, e.errors()))

            return ServiceResult(AppExceptionCase(500, f"The next error have occurred: {e}"))
