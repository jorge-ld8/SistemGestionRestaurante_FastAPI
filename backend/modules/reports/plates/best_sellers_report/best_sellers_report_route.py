from fastapi import APIRouter, Depends
from starlette import status

from modules.orders.repositories.read_model.order_rm_repository import OrderReadModelRepository as OrderRepository
from modules.reports.plates.best_sellers_report.best_sellers_report_service import BestSellersReportService
from shared.core.db.db_connection import get_db
from database import Session
from modules.users.user_auth.auth_decorators import authenticate_user, authorize_user
from modules.users.user_auth.auth_dependencies import get_current_user

from models import User

from shared.utils.service_result import handle_result

router = APIRouter()

def get_best_sellers_report_service():
    db: Session = next(get_db())
    order_repository = OrderRepository(db)
    return BestSellersReportService(order_repository)

@router.get("/best-sellers-report", status_code=status.HTTP_200_OK, name="Reports:Get Best Sellers Report")
@authenticate_user()
@authorize_user(["admin"])
async def get_best_sellers_report(
    service: BestSellersReportService = Depends(get_best_sellers_report_service),
    current_user: User = Depends(get_current_user)
):
    result = await service.get_best_sellers_report()
    return handle_result(result)