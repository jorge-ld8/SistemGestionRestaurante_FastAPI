from modules.users.repositories.user_repository import UserRepository
from shared.utils.app_exceptions import AppExceptionCase
from shared.utils.service_result import handle_result, ServiceResult


class DeleteUserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def delete_user(self, user_id: int) -> ServiceResult:
        try:
            saving_result = await self.repository.delete_user(user_id)

            if not saving_result.success:
                handle_result(saving_result)

            return ServiceResult("The user has  been deleted!")

        except Exception as e:
            if hasattr(e, 'errors') and callable(e.errors):
                return ServiceResult(AppExceptionCase(400, e.errors()))

            return ServiceResult(AppExceptionCase(500, f"The next error have occurred: {e}"))
