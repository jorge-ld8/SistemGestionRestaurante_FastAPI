from sqlalchemy import and_
from sqlalchemy.orm import Session
from starlette import status
from shared.utils.service_result import ServiceResult, handle_result
from shared.utils.app_exceptions import AppExceptionCase
from modules.users.schemas.domain import User
from models.user import User as UserModel


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    async def register_user(self, user: User) -> ServiceResult:
        try:
            db_user = UserModel(
                name=user.name,
                last_name=user.last_name,
                user_name=user.user_name,
                role=user.role,
            )

            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return ServiceResult("The user has been registered!!")

        except Exception as e:
            print(f"An error occurred: {e}")
            self.db.rollback()
            return ServiceResult(AppExceptionCase(500, str(e)))

    async def get_user_by_id(self, user_id: int) -> ServiceResult:
        try:
            user: UserModel = self.db.query(UserModel).filter(and_(UserModel.user_id == user_id,
                                                              UserModel.is_deleted == False)).one_or_none()
            if user is None:
                return ServiceResult(None)

            returned_user = User(user_id=user.user_id,
                                 name=user.name,
                                 last_name=user.last_name,
                                 user_name=user.user_name,
                                 role=user.role)

            return ServiceResult(returned_user)

        except Exception as e:
            print(f"An error occurred: {e}")
            return ServiceResult(AppExceptionCase(500, str(e)))

    async def update_user(self, user: User) -> ServiceResult:
        try:
            db_user: User = self.db.query(UserModel).filter(and_(UserModel.user_id == user.user_id,
                                                                 UserModel.is_deleted == False)).one_or_none()

            if db_user is None:
                return ServiceResult(AppExceptionCase(status.HTTP_404_NOT_FOUND, "User does not exist"))

            db_user.name = user.name
            db_user.last_name = user.last_name
            db_user.user_name = user.user_name
            db_user.role = user.role

            self.db.commit()
            self.db.refresh(db_user)

            return ServiceResult("The user has been updated!")

        except Exception as e:
            print(f"An error occurred: {e}")
            self.db.rollback()
            return ServiceResult(AppExceptionCase(500, str(e)))

    async def delete_user(self, user_id: int) -> ServiceResult:
        try:
            db_user: User = self.db.query(UserModel).filter(
                UserModel.user_id == user_id and UserModel.is_deleted is False).one_or_none()

            if db_user is None:
                return ServiceResult(AppExceptionCase(status.HTTP_404_NOT_FOUND, "User does not exist"))

            db_user.is_deleted = True
            self.db.commit()
            self.db.refresh(db_user)

            return ServiceResult("The user has been deleted!")

        except Exception as e:
            print(f"An error occurred: {e}")
            self.db.rollback()
            return ServiceResult(AppExceptionCase(500, str(e)))
