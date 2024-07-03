from sqlalchemy import func
from sqlalchemy.orm import Session

from shared.utils.service_result import ServiceResult
from shared.utils.app_exceptions import AppExceptionCase
from modules.orders.schemas.domain import Order
from models.order import Order as OrderModel
from models.waiter import Waiter as WaiterModel
from models import OrderDetail as OrderDetailModel
from models.plate import Plate as PlateModel
from models.plate_menu import PlatesMenu as PlatesMenuModel

class OrderReadModelRepository:
    def __init__(self, db: Session):
        self.db = db
    
    async def get_best_waiters_report(self) -> ServiceResult:
        try:
            waiters = (
                self.db.query(
                    WaiterModel.name,
                    WaiterModel.last_name,
                    func.count(OrderModel.order_id).label('order_count')
                )
                .join(OrderModel, OrderModel.waiter_id == WaiterModel.waiter_id)
                .filter(WaiterModel.is_deleted == False, OrderModel.is_deleted == False)
                .group_by(WaiterModel.waiter_id)
                .order_by(func.count(OrderModel.order_id).desc())
                .all()
            )
            return ServiceResult(waiters)
        except Exception as e:
            print(f"An error occurred: {e}")
            return ServiceResult(AppExceptionCase(500, e))
    

    async def get_best_sellers_report(self) -> ServiceResult:
        try:
            plate_menus = (
                self.db.query(
                    OrderDetailModel.plates_menu_id,
                    func.sum(OrderDetailModel.quantity).label('total_quantity')
                )
                .group_by(OrderDetailModel.plates_menu_id)
                .order_by(func.sum(OrderDetailModel.quantity).desc())
                .all()
            )
            
            result = []
            for plate_menu in plate_menus:
                plate_menu_id = plate_menu['plates_menu_id']
                total_quantity = plate_menu['total_quantity']
                plate_menu_info = self.db.query(PlatesMenuModel).filter(PlatesMenuModel.plate_menu_id == plate_menu_id).first()
                if plate_menu_info:
                    # plate_id = plate_menu_info.plate_id
                    menu_id = plate_menu_info.menu_id
                    plate = plate_menu_info.plate
                    result.append({
                        'plates_menu_id': plate_menu_id,
                        'total_quantity': total_quantity,
                        'plate': plate.name,
                        'menu': menu_id
                    })

            return ServiceResult(result)
        except Exception as e:
            print(f"An error occurred: {e}")
            return ServiceResult(AppExceptionCase(500, e))