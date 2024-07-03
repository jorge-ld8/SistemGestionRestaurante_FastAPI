from fastapi import APIRouter

from modules.reports.ingredients.ingredients_stock_report.ingredients_stock_report_route import router as ingredients_stock_report_router

ingredients_report_routes = APIRouter(
    prefix="/ingredients-reports",
    tags=["ingredients-reports"],
    responses={404: {"description": "Not found"}},
)

ingredients_report_routes.include_router(ingredients_stock_report_router)