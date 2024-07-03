from modules.users.repositories.user_repository import UserRepository
from shared.utils.app_exceptions import AppExceptionCase
from shared.utils.service_result import handle_result, ServiceResult


class GetUserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_user_by_id(self, user_id: int) -> ServiceResult:
        try:
            user_result = handle_result(await self.repository.get_user_by_id(user_id))

            if user_result is None:
                return ServiceResult("user not found")

            return ServiceResult(user_result)

        except Exception as e:
            if hasattr(e, 'errors') and callable(e.errors):
                return ServiceResult(AppExceptionCase(400, e.errors()))

            return ServiceResult(AppExceptionCase(500, f"The next error has occurred: {e}"))
