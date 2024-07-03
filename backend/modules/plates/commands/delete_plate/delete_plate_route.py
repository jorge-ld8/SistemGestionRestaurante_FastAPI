from fastapi import APIRouter, Depends
from starlette import status

from modules.plates.repositories.write_model.plate_wm_repository import PlateWriteModelRepository as PlateRepository
from modules.plates.commands.delete_plate.delete_plate_service import DeletePlateService
from shared.core.db.db_connection import get_db
from database import Session

from shared.utils.service_result import handle_result

router = APIRouter()

def delete_plate_service():
    db: Session = next(get_db())
    plate_repository = PlateRepository(db)
    return DeletePlateService(plate_repository)

@router.delete("/{plate_id}", status_code=status.HTTP_200_OK, name = "plates:delete_plate")
async def delete_plate(
    plate_id: int,
    service: DeletePlateService = Depends(delete_plate_service)
):
    result = await service.delete_plate(plate_id)
    return handle_result(result)