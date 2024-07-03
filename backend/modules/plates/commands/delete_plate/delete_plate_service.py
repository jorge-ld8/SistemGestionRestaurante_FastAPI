from shared.utils.service_result import ServiceResult, handle_result
from modules.plates.repositories.write_model.plate_wm_repository import PlateWriteModelRepository as PlateRepository
from shared.utils.app_exceptions import AppExceptionCase

class DeletePlateService:
    def __init__(self, plateRepository: PlateRepository):
        self.plateRepository = plateRepository

    async def delete_plate(self, plate_id: int):
        try:
            delete_result = await self.plateRepository.delete_plate(plate_id)

            handle_result(delete_result)

            return ServiceResult("The plate have been deleted!!")

        except Exception as e:

            if (e.status_code):
                return ServiceResult(AppExceptionCase(e.status_code, e.msg))
            
            return ServiceResult(AppExceptionCase(500, f"The next error have ocurred: {e}"))