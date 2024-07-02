from modules.users.schemas.dtos import UpdateUser
from modules.users.schemas.domain import User
from modules.users.repositories.user_repository import UserRepository
from shared.utils.app_exceptions import AppExceptionCase
from shared.utils.service_result import handle_result, ServiceResult


class UpdateUserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def update_user(self, user: UpdateUser, user_id: int) -> ServiceResult:
        try:
            user_result: User = handle_result(await self.repository.get_user_by_id(user_id))

            if user_result is None:
                return ServiceResult("User not found")

            new_user = User(
                user_id=0,
                name=user.name if user.name is not None else user_result.name,
                last_name=user.last_name if user.last_name is not None else user_result.last_name,
                user_name=user.user_name if user.user_name is not None else user_result.user_name,
                role=user.role if user.role is not None else user_result.role,
            )

            saving_result = await self.repository.update_user(new_user, user_id)

            if not saving_result.success:
                handle_result(saving_result)

            return ServiceResult("The user has been updated")

        except Exception as e:
            if hasattr(e, 'errors') and callable(e.errors):
                return ServiceResult(AppExceptionCase(400, e.errors()))

            return ServiceResult(AppExceptionCase(500, f"The next error have occurred: {e}"))
