from fastapi import APIRouter, Body, Depends, status

from modules.chefs.queries.get_chef_by_id.get_chef_service import GetChefService
from modules.chefs.repositories.chef_repository import ChefRepository
from shared.core.db.db_connection import get_db
from database import Session, Base
from shared.utils.service_result import handle_result

router = APIRouter()


def get_chef_by_id_service():
    db: Session = next(get_db())
    repository = ChefRepository(db)
    return GetChefService(repository)


@router.get("/{chef_id}", status_code=status.HTTP_200_OK, name="chefs:get-chef-by-id")
async def get_chef_by_id(
    chef_id: int,
    service: GetChefService = Depends(get_chef_by_id_service)
):
    result = await service.get_chef_by_id(chef_id)
    return handle_result(result)
