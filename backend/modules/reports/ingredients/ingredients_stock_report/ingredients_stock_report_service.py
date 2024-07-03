from shared.utils.service_result import ServiceResult, handle_result

from modules.ingredients.repositories.read_model.ingredient_rm_repository import IngredientReadModelRepository as IngredientRepository
from shared.utils.app_exceptions import AppExceptionCase

class GetIngredientsReportService:
    
        def __init__(self, ingredientRepository: IngredientRepository):
            self.ingredientRepository = ingredientRepository
    
        async def get_ingredients_report(self):
            try:
    
                ingredients_search_result = await self.ingredientRepository.get_ingredients_stock_report()
    
                ingredients = handle_result(ingredients_search_result)
    
                if ingredients is None:
                    return ServiceResult(AppExceptionCase(404, "There are no ingredients registered"))
    
                return ServiceResult(ingredients)
    
            except Exception as e:
                if(hasattr(e, 'errors') and callable(e.errors)):
                    return ServiceResult(AppExceptionCase(400, e.errors()))
    
                if(e.status_code):
                    return ServiceResult(AppExceptionCase(e.status_code, e.msg))
    
                return ServiceResult(AppExceptionCase(500, f"The next error have ocurred: {e}"))
