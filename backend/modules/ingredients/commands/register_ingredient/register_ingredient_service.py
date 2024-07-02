from modules.ingredients.schemas.dtos import RegisterIngredient
from modules.ingredients.schemas.domain import Ingredient
from modules.ingredients.repositories.ingredient_repository import IngredientRepository
from shared.utils.app_exceptions import AppExceptionCase
from shared.utils.service_result import handle_result, ServiceResult


class RegisterIngredientService:
    
    def __init__(self, repository: IngredientRepository):
        self.repository = repository
    
    async def register_ingredient(self, ingredient: RegisterIngredient) -> ServiceResult:
        try:
            newIngredient = Ingredient(
                name=ingredient.name,
                stock=ingredient.stock,
                unit=ingredient.unit,
                description=ingredient.description
            )

            savingResult = await self.repository.register_ingredient(newIngredient)

            if not savingResult.success:
                handle_result(savingResult)
            
            return ServiceResult("The ingredient have been registered!!")
            
        except Exception as e:
            if(hasattr(e, 'errors') and callable(e.errors)):
                return ServiceResult(AppExceptionCase(400, e.errors()))
            
            return ServiceResult(AppExceptionCase(500, f"The next error have ocurred: {e}"))
        