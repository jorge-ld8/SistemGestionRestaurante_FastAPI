from shared.utils.service_result import ServiceResult, handle_result
from modules.plates.schemas.dtos import RegisterPlate
from modules.plates.schemas.domain import Plate, PlateIngredient
from modules.plates.repositories.write_model.plate_wm_repository import PlateWriteModelRepository as PlateRepository
from modules.ingredients.repositories.ingredient_repository import IngredientRepository
from shared.utils.app_exceptions import AppExceptionCase

class RegisterPlateService:

    def __init__(self, plateRepository: PlateRepository, ingredientRepository: IngredientRepository):
        self.plateRepository = plateRepository
        self.ingredientRepository = ingredientRepository
    
    async def register_plate(self, dto: RegisterPlate):
        try:

            ingredientes_search_result = await self.ingredientRepository.get_ingredients_by_ids([ingredient.ingredientId for ingredient in dto.ingredients])
            
            ingredients = handle_result(ingredientes_search_result)

            plate_ingredients = []

            for ingredient in ingredients:
                plate_ingredients.append(PlateIngredient(
                    ingredient=ingredient,
                    quantity=[ingredient_dto.quantity for ingredient_dto in dto.ingredients if ingredient_dto.ingredientId == ingredient.id][0]
                ))

            newPlate = Plate(
                id=0,
                name=dto.name,
                description=dto.description,
                ingredients=plate_ingredients
            )

            
            savingResult = await self.plateRepository.register_plate(newPlate)

            if not savingResult.success:
                handle_result(savingResult)
            
            return ServiceResult("The plate have been registered!!")
            
        except Exception as e:
            if(hasattr(e, 'errors') and callable(e.errors)):
                return ServiceResult(AppExceptionCase(400, e.errors()))
            
            if(e.status_code):
                return ServiceResult(AppExceptionCase(e.status_code, e.msg))
            
            return ServiceResult(AppExceptionCase(500, f"The next error have ocurred: {e}"))