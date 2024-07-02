from fastapi import APIRouter, Body, Depends
from modules.chefs.commands.update_chef.update_chef_service import UpdateChefService
from modules.chefs.repositories.chef_repository import ChefRepository
from modules.chefs.schemas.dtos import UpdateChef
from shared.core.db.db_connection import get_db
from database import Session, Base
from fastapi import status
from shared.utils.service_result import ServiceResult, handle_result

router = APIRouter()


def update_chef_service():
    db: Session = next(get_db())
    repository = ChefRepository(db)
    return UpdateChefService(repository)


@router.put("/{chef_id}", status_code=status.HTTP_200_OK)
async def update_chef(
    chef_id: int,
    chef: UpdateChef = Body(..., embed=True),
    service: UpdateChefService = Depends(update_chef_service)
):
    result = await service.update_chef(chef, chef_id)
    return handle_result(result)
