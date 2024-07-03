from shared.utils.service_result import ServiceResult, handle_result
from modules.plates.schemas.dtos import AdjustIngredientQuantity
from modules.plates.schemas.domain import Plate, PlateIngredient
from modules.plates.repositories.plate_repository import PlateRepository
from modules.ingredients.repositories.ingredient_repository import IngredientRepository
from shared.utils.app_exceptions import AppExceptionCase


class AdjustIngredientQuantityService:

     def __init__(self, plateRepository: PlateRepository, ingredientRepository: IngredientRepository):
        self.plateRepository = plateRepository
        self.ingredientRepository = ingredientRepository

     async def adjust_ingredient_quantity(self, plate_id: int, ingredient_id: int, dto: AdjustIngredientQuantity):
        try:

            plate_ingredient_search_result = await self.plateRepository.get_plate_ingredient(plate_id, ingredient_id)

            plate_ingredient = handle_result(plate_ingredient_search_result)

            if plate_ingredient is None:
                return ServiceResult(AppExceptionCase(404, "That plate with that ingredient does not exist"))

            ingredient_search_result = await self.ingredientRepository.get_ingredient_by_id(ingredient_id)

            ingredient = handle_result(ingredient_search_result)

            if ingredient is None:
                return ServiceResult(AppExceptionCase(404, "The ingredient does not exist"))
            
            updated_plate_ingredient = PlateIngredient(
                ingredient=ingredient,
                quantity=plate_ingredient.quantity + dto.quantity
            )

            savingResult = await self.plateRepository.adjust_ingredient_quantity(plate_id, updated_plate_ingredient)

            return ServiceResult(savingResult.value)
            if not savingResult.success:
                handle_result(savingResult)
            return ServiceResult("The ingredient quantity have been adjusted!!")

        except Exception as e:
            if(hasattr(e, 'errors') and callable(e.errors)):
                return ServiceResult(AppExceptionCase(400, e.errors()))
            
            if(e.status_code):
                return ServiceResult(AppExceptionCase(e.status_code, e.msg))
            
            return ServiceResult(AppExceptionCase(500, f"The next error have ocurred: {e}"))
