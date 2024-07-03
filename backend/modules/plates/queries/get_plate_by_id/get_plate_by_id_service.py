from shared.utils.service_result import ServiceResult, handle_result
from modules.plates.schemas.domain import Plate, PlateIngredient
from modules.plates.repositories.read_model.plate_rm_repository import PlateReadModelRepository as PlateRepository

from modules.ingredients.repositories.ingredient_repository import IngredientRepository

from shared.utils.app_exceptions import AppExceptionCase

class GetPlateByIdService:

    def __init__(self, plateRepository: PlateRepository):
        self.plateRepository = plateRepository

    async def get_plate_by_id(self, plate_id: int):
        try:

            plate_search_result = await self.plateRepository.get_plate_by_id(plate_id)

            plate = handle_result(plate_search_result)

            if plate is None:
                return ServiceResult(AppExceptionCase(404, "The plate does not exist"))
            
            return ServiceResult(plate)
            
        except Exception as e:
            if(hasattr(e, 'errors') and callable(e.errors)):
                return ServiceResult(AppExceptionCase(400, e.errors()))
            
            if(e.status_code):
                return ServiceResult(AppExceptionCase(e.status_code, e.msg))
            
            return ServiceResult(AppExceptionCase(500, f"The next error have ocurred: {e}"))