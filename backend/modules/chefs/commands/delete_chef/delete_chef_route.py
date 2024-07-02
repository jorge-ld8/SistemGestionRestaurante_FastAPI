from fastapi import APIRouter, Body, Depends
from modules.chefs.commands.delete_chef.delete_chef_service import DeleteChefService
from modules.chefs.repositories.chef_repository import ChefRepository
from shared.core.db.db_connection import get_db
from database import Session, Base
from fastapi import status
from shared.utils.service_result import ServiceResult, handle_result

router = APIRouter()


def delete_chef_service():
    db: Session = next(get_db())
    repository = ChefRepository(db)
    return DeleteChefService(repository)


@router.delete("/{chef_id}", status_code=status.HTTP_200_OK)
async def delete_chef(
    chef_id: int,
    service: DeleteChefService = Depends(delete_chef_service)
):
    result = await service.delete_chef(chef_id)
    return handle_result(result)
