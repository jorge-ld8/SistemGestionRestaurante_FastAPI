from fastapi import APIRouter, Body, Depends
from starlette import status

from modules.ingredients.repositories.ingredient_repository import IngredientRepository
from modules.plates.repositories.write_model.plate_wm_repository import PlateWriteModelRepository as PlateRepository
from modules.plates.schemas.dtos import AdjustIngredientQuantity
from modules.plates.commands.adjust_ingredient_quantity.adjust_ingredient_quantity_service import AdjustIngredientQuantityService
from shared.core.db.db_connection import get_db
from database import Session

from shared.utils.service_result import handle_result

router = APIRouter()

def adjust_ingredient_quantity_service():
    db: Session = next(get_db())
    plate_repository = PlateRepository(db)
    ingredient_repository = IngredientRepository(db)
    return AdjustIngredientQuantityService(plate_repository, ingredient_repository)

@router.put("/{plate_id}/ingredient/{ingredient_id}", status_code=status.HTTP_200_OK, name = "plates:adjust_ingredient_quantity")
async def adjust_ingredient_quantity(
    plate_id: int,
    ingredient_id: int,
    quantity: AdjustIngredientQuantity = Body(..., embed=True),
    service: AdjustIngredientQuantityService = Depends(adjust_ingredient_quantity_service)
):
    result = await service.adjust_ingredient_quantity(plate_id, ingredient_id, quantity)
    return handle_result(result)