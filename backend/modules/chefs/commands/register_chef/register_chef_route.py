from fastapi import APIRouter, Body, Depends
from starlette import status
from modules.chefs.repositories.chef_repository import ChefRepository
from modules.chefs.schemas.dtos import RegisterChef
from modules.chefs.commands.register_chef.register_chef_service import RegisterChefService
from shared.core.db.db_connection import get_db
from database import Session, Base

from shared.utils.service_result import ServiceResult, handle_result

router = APIRouter()


def register_chef_service():
    db: Session = next(get_db())
    repository = ChefRepository(db)
    return RegisterChefService(repository)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def register_chef(
    chef: RegisterChef = Body(..., embed=True), 
    service: RegisterChefService = Depends(register_chef_service)
):
    result = await service.register_chef(chef)
    return handle_result(result)
