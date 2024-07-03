from fastapi import APIRouter, Body, Depends
from starlette import status

from modules.plates.repositories.write_model.plate_wm_repository import PlateWriteModelRepository as PlateRepository
from modules.plates.schemas.dtos import UpdatePlate
from modules.plates.commands.update_plate.update_plate_service import UpdatePlateService
from shared.core.db.db_connection import get_db
from database import Session

from shared.utils.service_result import handle_result

router = APIRouter()

def update_plate_service():
    db: Session = next(get_db())
    plate_repository = PlateRepository(db)
    return UpdatePlateService(plate_repository)

@router.put("/{plate_id}", status_code=status.HTTP_200_OK, name = "plates:update_plate")
async def update_plate(
    plate_id: int,
    plate: UpdatePlate = Body(..., embed=True),
    service: UpdatePlateService = Depends(update_plate_service)
):
    result = await service.update_plate(plate_id, plate)
    return handle_result(result)