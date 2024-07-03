from fastapi import APIRouter, Depends
from starlette import status

from modules.ingredients.repositories.ingredient_repository import IngredientRepository
# from modules.plates.repositories.plate_repository import PlateRepository
from modules.plates.repositories.read_model.plate_rm_repository import PlateReadModelRepository as PlateRepository
from modules.plates.queries.get_plate_by_id.get_plate_by_id_service import GetPlateByIdService
from shared.core.db.db_connection import get_db
from database import Session

from shared.utils.service_result import handle_result

router = APIRouter()

def get_plate_by_id_service():
    db: Session = next(get_db())
    plate_repository = PlateRepository(db)
    return GetPlateByIdService(plate_repository)

@router.get("/{plate_id}", status_code=status.HTTP_200_OK, name = "plates:get_plate_by_id")
async def get_plate_by_id(
    plate_id: int,
    service: GetPlateByIdService = Depends(get_plate_by_id_service)
):
    result = await service.get_plate_by_id(plate_id)
    return handle_result(result)
