from fastapi import APIRouter

from modules.reports.plates.best_sellers_report.best_sellers_report_route import router as best_sellers_report_router

plates_report_routes = APIRouter(
    prefix="/plates_report",
    tags=["plates_report"],
    responses={404: {"description": "Not found"}},
)

plates_report_routes.include_router(best_sellers_report_router)