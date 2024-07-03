from shared.utils.service_result import ServiceResult, handle_result
from modules.plates.schemas.domain import Plate, PlateIngredient
from modules.plates.repositories.plate_repository import PlateRepository
from modules.ingredients.repositories.ingredient_repository import IngredientRepository

from shared.utils.app_exceptions import AppExceptionCase

class GetPlateByIdService:

    def __init__(self, plateRepository: PlateRepository, ingredientRepository: IngredientRepository):
        self.plateRepository = plateRepository
        self.ingredientRepository = ingredientRepository
    
    async def get_plate_by_id(self, plate_id: int):
        try:

            plate_search_result = await self.plateRepository.get_plate_basic_info_by_id(plate_id)
            
            plate = handle_result(plate_search_result)

            if plate is None:
                return ServiceResult(AppExceptionCase(404, "The plate does not exist"))
            
            plate_ingredients_search_result = await self.plateRepository.get_plate_ingredients_by_plate_id(plate_id)

            plate_ingredients = handle_result(plate_ingredients_search_result)

            ingredients_search_result = await self.ingredientRepository.get_ingredients_by_ids([plate_ingredient.ingredient_id for plate_ingredient in plate_ingredients])

            ingredients = handle_result(ingredients_search_result)
            
            domain_plate_ingredients = []

            for ingredient in ingredients:
                domain_plate_ingredients.append(PlateIngredient(
                    ingredient=ingredient,
                    quantity=[plate_ingredient.quantity for plate_ingredient in plate_ingredients if plate_ingredient.ingredient_id == ingredient.id][0]
                ))


            plate.ingredients = domain_plate_ingredients

            return ServiceResult(plate)
            
        except Exception as e:
            if(hasattr(e, 'errors') and callable(e.errors)):
                return ServiceResult(AppExceptionCase(400, e.errors()))
            
            if(e.status_code):
                return ServiceResult(AppExceptionCase(e.status_code, e.msg))
            
            return ServiceResult(AppExceptionCase(500, f"The next error have ocurred: {e}"))