from modules.users.schemas.dtos import RegisterUser
from modules.users.schemas.domain import User
from modules.users.repositories.user_repository import UserRepository
from shared.utils.app_exceptions import AppExceptionCase
from shared.utils.service_result import handle_result, ServiceResult


class RegisterUserService:
    
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    async def register_user(self, user: RegisterUser) -> ServiceResult:
        try:
            new_user = User(
                user_id=0,
                name=user.name,
                last_name=user.last_name,
                user_name=user.user_name,
                role=user.role,
                password=user.password
            )

            saving_result = await self.repository.register_user(new_user)

            if not saving_result.success:
                handle_result(saving_result)
            
            return ServiceResult("The user have been registered!!")
            
        except Exception as e:
            if hasattr(e, 'errors') and callable(e.errors):
                return ServiceResult(AppExceptionCase(400, e.errors()))
            
            return ServiceResult(AppExceptionCase(500, f"The next error have occurred: {e}"))
        