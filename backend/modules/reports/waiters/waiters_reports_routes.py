from fastapi import APIRouter

from modules.reports.waiters.best_waiters_report.best_waiter_report_route import router as best_waiter_report_router

waiters_report_routes = APIRouter(
    prefix="/waiters_report",
    tags=["waiters_report"],
    responses={404: {"description": "Not found"}},
)

waiters_report_routes.include_router(best_waiter_report_router)