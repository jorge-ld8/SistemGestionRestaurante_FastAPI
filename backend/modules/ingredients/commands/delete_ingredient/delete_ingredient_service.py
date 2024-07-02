from shared.utils.service_result import ServiceResult, handle_result
from modules.ingredients.repositories.ingredient_repository import IngredientRepository
from shared.utils.app_exceptions import AppExceptionCase

class DeleteIngredientService:
    def __init__(self, repository: IngredientRepository):
        self.repository = repository
    

    async def delete_ingredient(self, ingredient_id: int) -> ServiceResult:
        try:
            
            delete_result = await self.repository.delete_ingredient(ingredient_id)

            #Si viene con una excepcion, se levanta la excepcion. Sino retorna el valor
            handle_result(delete_result)

            return ServiceResult("The ingredient have been deleted!!")
        
        except Exception as e:
            if (e.status_code):
                return ServiceResult(AppExceptionCase(e.status_code, e.msg))
            
            return ServiceResult(AppExceptionCase(500, f"The next error have ocurred: {e}"));