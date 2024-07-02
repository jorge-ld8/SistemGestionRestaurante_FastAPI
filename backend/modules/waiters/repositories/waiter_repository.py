from sqlalchemy import and_
from sqlalchemy.orm import Session
from starlette import status
from shared.utils.service_result import ServiceResult, handle_result
from shared.utils.app_exceptions import AppExceptionCase
from modules.waiters.schemas.domain import Waiter
from models.waiter import Waiter as WaiterModel


class WaiterRepository:

    def __init__(self, db: Session):
        self.db = db

    async def register_waiter(self, waiter: Waiter) -> ServiceResult:
        try:
            db_waiter = WaiterModel(
                name=waiter.name,
                last_name=waiter.last_name
            )

            self.db.add(db_waiter)
            self.db.commit()
            self.db.refresh(db_waiter)
            return ServiceResult("The waiter has been registered!!")

        except Exception as e:
            print(f"An error occurred: {e}")
            self.db.rollback()
            return ServiceResult(AppExceptionCase(500, str(e)))

    async def get_waiter_by_id(self, waiter_id: int) -> ServiceResult:
        try:
            waiter: Waiter = self.db.query(WaiterModel).filter(and_(WaiterModel.waiter_id == waiter_id,
                                                                    WaiterModel.is_deleted == False)).one_or_none()
            return ServiceResult(waiter)

        except Exception as e:
            print(f"An error occurred: {e}")
            return ServiceResult(AppExceptionCase(500, str(e)))

    async def update_waiter(self, waiter: Waiter) -> ServiceResult:
        try:
            db_waiter: Waiter = self.db.query(WaiterModel).filter(
                WaiterModel.waiter_id == waiter.waiter_id and not WaiterModel.is_deleted).one_or_none()

            if db_waiter is None:
                return ServiceResult(AppExceptionCase(status.HTTP_404_NOT_FOUND, "Waiter does not exist"))

            db_waiter.name = waiter.name
            db_waiter.last_name = waiter.last_name

            self.db.commit()
            self.db.refresh(db_waiter)

            return ServiceResult("The waiter has been updated!")

        except Exception as e:
            print(f"An error occurred: {e}")
            self.db.rollback()
            return ServiceResult(AppExceptionCase(500, str(e)))

    async def delete_waiter(self, waiter_id: int) -> ServiceResult:
        try:
            db_waiter: Waiter = self.db.query(WaiterModel).filter(
                WaiterModel.waiter_id == waiter_id and WaiterModel.is_deleted is False).one_or_none()

            if db_waiter is None:
                return ServiceResult(AppExceptionCase(status.HTTP_404_NOT_FOUND, "Waiter does not exist"))

            db_waiter.is_deleted = True
            self.db.commit()
            self.db.refresh(db_waiter)

            return ServiceResult("The waiter has been deleted!")

        except Exception as e:
            print(f"An error occurred: {e}")
            self.db.rollback()
            return ServiceResult(AppExceptionCase(500, str(e)))
