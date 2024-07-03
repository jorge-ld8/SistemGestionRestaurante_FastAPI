from fastapi import APIRouter, Body, Depends
from starlette import status

from modules.ingredients.repositories.ingredient_repository import IngredientRepository
from modules.plates.repositories.write_model.plate_wm_repository import PlateWriteModelRepository as PlateRepository
from modules.plates.schemas.dtos import RegisterPlate
from modules.plates.commands.register_plate.register_plate_service import RegisterPlateService
from shared.core.db.db_connection import get_db
from database import Session
from modules.users.user_auth.auth_decorators import authenticate_user, authorize_user
from modules.users.user_auth.auth_dependencies import get_current_user

from models import User

from shared.utils.service_result import handle_result

router = APIRouter()

def register_plate_service():
    db: Session = next(get_db())
    plate_repository = PlateRepository(db)
    ingredient_repository = IngredientRepository(db)
    return RegisterPlateService(plate_repository, ingredient_repository)

@router.post("/", status_code=status.HTTP_201_CREATED, name = "plates:register_plate")
@authenticate_user()
@authorize_user(["admin"])
async def register_plate(
    plate: RegisterPlate = Body(..., embed=True),
    service: RegisterPlateService = Depends(register_plate_service),
    current_user: User = Depends(get_current_user)
):
    result = await service.register_plate(plate)
    return handle_result(result)