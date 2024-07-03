from fastapi import APIRouter

from modules.reports.ingredients.ingredients_reports_routes import ingredients_report_routes
from modules.reports.waiters.waiters_reports_routes import waiters_report_routes
from modules.reports.plates.plates_reports_routes import plates_report_routes

reports_routes = APIRouter(
    prefix="/reports",
    tags=["reports"],
    responses={404: {"description": "Not found"}},
)

reports_routes.include_router(ingredients_report_routes)
reports_routes.include_router(waiters_report_routes)
reports_routes.include_router(plates_report_routes)