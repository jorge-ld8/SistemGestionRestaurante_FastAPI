from sqlalchemy import and_
from sqlalchemy.orm import Session
from starlette import status
from shared.utils.service_result import ServiceResult, handle_result
from shared.utils.app_exceptions import AppExceptionCase
from modules.chefs.schemas.domain import Chef
from models.chef import Chef as ChefModel


class ChefRepository:

    def __init__(self, db: Session):
        self.db = db

    async def register_chef(self, chef: Chef) -> ServiceResult:
        try:
            db_chef = ChefModel(
                name=chef.name,
                last_name=chef.last_name
            )

            self.db.add(db_chef)
            self.db.commit()
            self.db.refresh(db_chef)
            return ServiceResult("The chef has been registered!!")

        except Exception as e:
            print(f"An error occurred: {e}")
            self.db.rollback()
            return ServiceResult(AppExceptionCase(500, str(e)))

    async def get_chef_by_id(self, chef_id: int) -> ServiceResult:
        try:
            chef: ChefModel = self.db.query(ChefModel).filter(and_(ChefModel.chef_id == chef_id,
                                                              ChefModel.is_deleted == False)).one_or_none()

            if chef is None:
                return ServiceResult(None)

            returned_chef = Chef(
                chef_id=chef_id,
                name=chef.name,
                last_name=chef.last_name
            )

            return ServiceResult(returned_chef)

        except Exception as e:
            print(f"An error occurred: {e}")
            return ServiceResult(AppExceptionCase(500, str(e)))

    async def update_chef(self, chef: Chef) -> ServiceResult:
        try:
            db_chef: Chef = self.db.query(ChefModel).filter(and_(ChefModel.chef_id == chef.chef_id,
                                                                 ChefModel.is_deleted == False)).one_or_none()

            if db_chef is None:
                return ServiceResult(AppExceptionCase(status.HTTP_404_NOT_FOUND, "Chef does not exist"))

            db_chef.name = chef.name
            db_chef.last_name = chef.last_name

            self.db.commit()
            self.db.refresh(db_chef)

            return ServiceResult("The chef has been updated!")

        except Exception as e:
            print(f"An error occurred: {e}")
            self.db.rollback()
            return ServiceResult(AppExceptionCase(500, str(e)))

    async def delete_chef(self, chef_id: int) -> ServiceResult:
        try:
            db_chef: Chef = self.db.query(ChefModel).filter(
                ChefModel.chef_id == chef_id and ChefModel.is_deleted is False).one_or_none()

            if db_chef is None:
                return ServiceResult(AppExceptionCase(status.HTTP_404_NOT_FOUND, "Chef does not exist"))

            db_chef.is_deleted = True
            self.db.commit()
            self.db.refresh(db_chef)

            return ServiceResult("The chef has been deleted!")

        except Exception as e:
            print(f"An error occurred: {e}")
            self.db.rollback()
            return ServiceResult(AppExceptionCase(500, str(e)))
