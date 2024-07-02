from sqlalchemy.orm import Session
from backend.shared.utils.service_result import ServiceResult
from backend.shared.utils.app_exceptions import AppExceptionCase
from backend.modules.orders.schemas.domain import Order
from backend.models.order import Order as OrderModel


class OrderRepository():

    def __init__(self, db: Session):
        self.db = db

    async def register_order(self, order: Order) -> ServiceResult:
        try:
            db_order = OrderModel(
                name=ingredient.name,
                stock=ingredient.stock,
                unit=ingredient.unit,
                description=ingredient.description
            )

            self.db.add(db_order)
            self.db.commit()
            self.db.refresh(db_order)
            return ServiceResult("The ingredient have been registered!!")

        except Exception as e:
            print(f"An error occurred: {e}")
            self.db.rollback()
            return ServiceResult(AppExceptionCase(500, e))
