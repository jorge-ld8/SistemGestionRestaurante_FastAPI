from shared.utils.service_result import ServiceResult, handle_result
from modules.ingredients.schemas.domain import Ingredient
from modules.ingredients.repositories.ingredient_repository import IngredientRepository
from shared.utils.app_exceptions import AppExceptionCase

class GetIngredientByIdService:
    def __init__(self, repository: IngredientRepository):
        self.repository = repository
    
    async def get_ingredient_by_id(self, ingredient_id: int) -> ServiceResult:
        try:
            get_ingredient_result = await self.repository.get_ingredient_by_id(ingredient_id)

            #Si viene con una excepcion, se levanta la excepcion. Sino retorna el valor
            ingredient = handle_result(get_ingredient_result)

            if ingredient is None:
                return ServiceResult(AppExceptionCase(404, "The ingredient does not exist"))
            

            return ServiceResult(ingredient)
        
        except Exception as e:
            return ServiceResult(AppExceptionCase(500, f"The next error have ocurred: {e}"))