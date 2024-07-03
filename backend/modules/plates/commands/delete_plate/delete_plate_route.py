from fastapi import APIRouter, Depends
from starlette import status

from modules.plates.repositories.write_model.plate_wm_repository import PlateWriteModelRepository as PlateRepository
from modules.plates.commands.delete_plate.delete_plate_service import DeletePlateService
from shared.core.db.db_connection import get_db
from database import Session
from modules.users.user_auth.auth_decorators import authenticate_user, authorize_user
from modules.users.user_auth.auth_dependencies import get_current_user

from models import User

from shared.utils.service_result import handle_result

router = APIRouter()

def delete_plate_service():
    db: Session = next(get_db())
    plate_repository = PlateRepository(db)
    return DeletePlateService(plate_repository)

@router.delete("/{plate_id}", status_code=status.HTTP_200_OK, name = "plates:delete_plate")
@authenticate_user()
@authorize_user(["admin"])
async def delete_plate(
    plate_id: int,
    service: DeletePlateService = Depends(delete_plate_service),
    current_user: User = Depends(get_current_user)
):
    result = await service.delete_plate(plate_id)
    return handle_result(result)