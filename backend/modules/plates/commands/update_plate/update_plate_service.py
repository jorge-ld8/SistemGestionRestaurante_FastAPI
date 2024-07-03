from shared.utils.service_result import ServiceResult, handle_result
from modules.plates.schemas.dtos import UpdatePlate
from modules.plates.schemas.domain import Plate
from modules.plates.repositories.write_model.plate_wm_repository import PlateWriteModelRepository as PlateRepository
from shared.utils.app_exceptions import AppExceptionCase

class UpdatePlateService:
    
        def __init__(self, plateRepository: PlateRepository):
            self.plateRepository = plateRepository
        
        async def update_plate(self, plate_id: int, dto: UpdatePlate):
            try:
    
                plate_search_result = await self.plateRepository.get_plate_basic_info_by_id(plate_id)
                
                old_plate = handle_result(plate_search_result)
    
                if old_plate is None:
                    return ServiceResult(AppExceptionCase(404, "The plate does not exist"))
                
                plate_updated = Plate(
                    id=old_plate.id,
                    name=dto.name if dto.name is not None else old_plate.name,
                    description=dto.description if dto.description is not None else old_plate.description,
                    ingredients=old_plate.ingredients #[]
                )
    
                savingResult = await self.plateRepository.update_plate(plate_updated)
    
                if not savingResult.success:
                    handle_result(savingResult)
                
                return ServiceResult("The plate have been updated!!")
                
            except Exception as e:
                if(hasattr(e, 'errors') and callable(e.errors)):
                    return ServiceResult(AppExceptionCase(400, e.errors()))
                
                if(e.status_code):
                    return ServiceResult(AppExceptionCase(e.status_code, e.msg))
                
                return ServiceResult(AppExceptionCase(500, f"The next error have ocurred: {e}"))
