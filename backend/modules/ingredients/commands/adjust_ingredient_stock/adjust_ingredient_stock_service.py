from shared.utils.service_result import ServiceResult, handle_result
from modules.ingredients.schemas.domain import Ingredient
from modules.ingredients.repositories.ingredient_repository import IngredientRepository
from shared.utils.app_exceptions import AppExceptionCase
from modules.ingredients.schemas.dtos import AdjustIngredientStock

class AdjustIngredientStockService:
    def __init__(self, repository: IngredientRepository):
        self.repository = repository

    async def adjust_ingredient_stock(self, ingredient_id: int, dto: AdjustIngredientStock) -> ServiceResult:
        try:
            get_ingredient_result = await self.repository.get_ingredient_by_id(ingredient_id)
            
            old_ingredient = handle_result(get_ingredient_result)

            if old_ingredient is None:
                return ServiceResult(AppExceptionCase(404, "The ingredient does not exist"))

            ingredient_adjusted = Ingredient(
                id=old_ingredient.id,
                name=old_ingredient.name,
                stock=old_ingredient.stock + dto.stock,
                unit=old_ingredient.unit,
                description=old_ingredient.description
            )

            savingResult = await self.repository.adjust_ingredient_stock(ingredient_adjusted)

            if not savingResult.success:
                handle_result(savingResult)

            return ServiceResult("The ingredient stock have been adjusted!!")
        
        except Exception as e:
            if(hasattr(e, 'errors') and callable(e.errors)):
                return ServiceResult(AppExceptionCase(400, e.errors()))
            
            return ServiceResult(AppExceptionCase(500, f"The next error have ocurred: {e}"))
