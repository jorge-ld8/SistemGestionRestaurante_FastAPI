from sqlalchemy import and_
from sqlalchemy.orm import Session

from shared.utils.service_result import ServiceResult
from shared.utils.app_exceptions import AppExceptionCase
from modules.orders.schemas.domain import Order
from models.order import Order as OrderModel
from models import OrderDetail as OrderDetailModel
from starlette import status


class OrderRepository:

    def __init__(self, db: Session):
        self.db = db

    async def register_order(self, order: Order) -> ServiceResult:
        try:
            db_order = OrderModel(
                estado=order.status,
                datetime=order.datetime,
                total=order.total,
                user_id=order.user_id,
                chef_id=order.chef_id,
                waiter_id=order.waiter_id
            )
            self.db.add(db_order)
            self.db.commit()

            for order_detail in order.order_details:
                print(order_detail)
                db_order_detail = OrderDetailModel(
                    quantity=order_detail.quantity,
                    order_id=db_order.order_id,
                    plates_menu_id=order_detail.plate_menu_id
                )
                print(f'quantity: {order_detail.quantity}')
                print(f'plates_menu_id: {order_detail.plate_menu_id}')
                print(f'order_id: {db_order.order_id}')
                self.db.add(db_order_detail)

            self.db.commit()
            self.db.refresh(db_order)
            return ServiceResult("The order has been registered!")

        except Exception as e:
            print(f"An error occurred: {e}")
            self.db.rollback()
            return ServiceResult(AppExceptionCase(500, e))

    async def get_order_by_id(self, order_id: int) -> ServiceResult:
        try:
            order: OrderModel = self.db.query(OrderModel).filter(and_(OrderModel.order_id == order_id,
                                                                      OrderModel.is_deleted == False)).one_or_none()

            if order is None:
                return ServiceResult(None)

            returned_order = Order(
                order_id=order_id,
                user_id=order.user_id,
                chef_id=order.chef_id,
                waiter_id=order.waiter_id,
                datetime=order.datetime,
                status=order.estado,
                total=order.total,
                order_details=order.order_details
            )

            return ServiceResult(returned_order)

        except Exception as e:
            print(f"An error occurred: {e}")
            return ServiceResult(AppExceptionCase(500, str(e)))

    async def update_order(self, order: Order) -> ServiceResult:
        try:
            db_order: OrderModel = self.db.query(OrderModel).filter(and_(OrderModel.order_id == order.order_id,
                                                                         OrderModel.is_deleted == False)).one_or_none()

            if db_order is None:
                return ServiceResult(AppExceptionCase(status.HTTP_404_NOT_FOUND, "Order does not exist"))

            db_order.estado = order.status

            self.db.commit()
            self.db.refresh(db_order)

            return ServiceResult(f'The order has been {order.status}!')

        except Exception as e:
            print(f"An error occurred: {e}")
            self.db.rollback()
            return ServiceResult(AppExceptionCase(500, str(e)))
