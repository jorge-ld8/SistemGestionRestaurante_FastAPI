
from shared.utils.service_result import ServiceResult, handle_result
from modules.ingredients.schemas.dtos import RegisterIngredient
from modules.ingredients.schemas.domain import Ingredient
from modules.ingredients.repositories.ingredient_repository import IngredientRepository
from shared.utils.app_exceptions import AppExceptionCase


class RegisterIngredientService:
    
    def __init__(self, repository: IngredientRepository):
        self.repository = repository
    
    async def register_ingredient(self, dto: RegisterIngredient) -> ServiceResult:
        try:

            
            #Como es la creacion, se pone en 0 el id y en el repo se cambia a autoincremental
            newIngredient = Ingredient(
                id=0,
                name=dto.name,
                stock=dto.stock,
                unit=dto.unit,
                description=dto.description
            )

            savingResult = await self.repository.register_ingredient(newIngredient)

            #Aca pudiera hacer return handle_result(savingResult) pero estaria retornando
            #como resultado del caso de uso, la respuesta del repositorio y so esta niche
            if not savingResult.success:
                handle_result(savingResult)
            
            
            return ServiceResult("The ingredient have been registered!!")
            
        except Exception as e:
            if(hasattr(e, 'errors') and callable(e.errors)):
                return ServiceResult(AppExceptionCase(400, e.errors()))
            
            return ServiceResult(AppExceptionCase(500, f"The next error have ocurred: {e}"))
        