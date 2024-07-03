from datetime import datetime
from typing import List
from modules.orders.schemas.domain import Order
from modules.orders.schemas.domain import OrderDetail
from shared.utils.app_exceptions import AppExceptionCase
from modules.orders.schemas.dtos import RegisterOrder
from shared.utils.service_result import handle_result, ServiceResult
from modules.orders.repositories.order_repository import OrderRepository

from modules.chefs.repositories.chef_repository import ChefRepository
from modules.users.repositories.user_repository import UserRepository
from modules.waiters.repositories.waiter_repository import WaiterRepository
from modules.menus.repositories.write_model.menu_wm_repository import MenuWriteModelRepository
from modules.menus.schemas.domain import PlateMenu


class RegisterOrderService:

    def __init__(self,
                 order_repo: OrderRepository,
                 user_repo: UserRepository,
                 waiter_repo: WaiterRepository,
                 chef_repo: ChefRepository,
                 menu_repo: MenuWriteModelRepository
                 ):
        self.order_repo = order_repo
        self.user_repo = user_repo
        self.waiter_repo = waiter_repo
        self.chef_repo = chef_repo
        self.menu_repo = menu_repo

    async def register_order(self, order: RegisterOrder) -> ServiceResult:
        try:
            user = handle_result(await self.user_repo.get_user_by_id(order.user_id))
            if user is None:
                return ServiceResult(AppExceptionCase(404, "The user does not exist"))

            waiter = handle_result(await self.waiter_repo.get_waiter_by_id(order.waiter_id))
            if waiter is None:
                return ServiceResult(AppExceptionCase(404, "The waiter does not exist"))

            chef = handle_result(await self.chef_repo.get_chef_by_id(order.chef_id))
            if chef is None:
                return ServiceResult(AppExceptionCase(404, "The chef does not exist"))

            # check if list of plates are available, like next line
            if not handle_result(await self.menu_repo.check_plates_availability(order.plates)):
                return ServiceResult(AppExceptionCase(404, "At least one plate does not have enough stock to be made"))

            order_details_list: List[OrderDetail] = []
            total = 0
            for plate in order.plates:
                plate_menu: PlateMenu = handle_result(await self.menu_repo.get_plate_menu_by_id(plate.plate_menu_id))
                plate_menu_price = plate_menu.unit_price
                total += plate_menu_price * plate.quantity
                order_details_list.append(
                    OrderDetail(
                        quantity=plate.quantity,
                        plate_menu_id=plate.plate_menu_id,
                    )
                )

            # Create new order
            new_order: Order = Order(
                order_id=0,
                user_id=order.user_id,
                chef_id=order.chef_id,
                waiter_id=order.waiter_id,
                order_details=order_details_list,
                status="preparing",
                datetime=datetime.now(),
                total=total)

            saving_result = await self.order_repo.register_order(new_order)

            if not saving_result.success:
                handle_result(saving_result)

            return ServiceResult("The order has been registered!")

        except Exception as e:
            if hasattr(e, 'errors') and callable(e.errors):
                return ServiceResult(AppExceptionCase(400, e.errors()))

            return ServiceResult(AppExceptionCase(500, f"The next error have occurred: {e}"))

    # async def get_plate_price(self, plate_id) -> int:
    #     try:
    #
    #     except Exception as e:
    #         if hasattr(e, 'errors') and callable(e.errors):
    #             return ServiceResult(AppExceptionCase(400, e.errors()))


