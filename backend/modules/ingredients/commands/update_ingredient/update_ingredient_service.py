from shared.utils.service_result import ServiceResult, handle_result
from modules.ingredients.schemas.domain import Ingredient
from modules.ingredients.repositories.ingredient_repository import IngredientRepository
from shared.utils.app_exceptions import AppExceptionCase
from modules.ingredients.schemas.dtos import UpdateIngredient


class UpdateIngredientService:
    def __init__(self, repository: IngredientRepository):
        self.repository = repository

    async def update_ingredient(self, ingredient_id: int, dto: UpdateIngredient) -> ServiceResult:

        try:

            get_ingredient_result = await self.repository.get_ingredient_by_id(ingredient_id)
            
            #Si viene con una excepcion, se levanta la excepcion. Sino retorna el valor
            old_ingredient = handle_result(get_ingredient_result)

            # #Si no se encontro el ingrediente, se lanza una excepcion
            if old_ingredient is None:
                return ServiceResult(AppExceptionCase(404, "The ingredient does not exist"))
            
            #Se actualiza el ingrediente generando uno nuevo con las nuevas propiedades (y validandolas)
            new_ingredient = Ingredient(
                id=old_ingredient.id,
                name=dto.name if dto.name is not None else old_ingredient.name,
                stock=old_ingredient.stock,#No se actualiza el stock
                unit=dto.unit if dto.unit is not None else old_ingredient.unit,
                description=dto.description if dto.description is not None else old_ingredient.description
            )

            savingResult = await self.repository.update_ingredient(new_ingredient)

            # #Aca pudiera hacer return handle_result(savingResult) pero estaria retornando
            # #como resultado del caso de uso, la respuesta del repositorio y eso esta niche
            if not savingResult.success:
                handle_result(savingResult)

            return ServiceResult("The ingredient have been updated!!")
        
        except Exception as e:
            if(hasattr(e, 'errors') and callable(e.errors)):
                return ServiceResult(AppExceptionCase(400, e.errors()))
            
            return ServiceResult(AppExceptionCase(500, f"The next error have ocurred: {e}"))
