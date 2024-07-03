from functools import wraps
from fastapi import HTTPException, status
from models import User


def authenticate_user():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user: User = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated"
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def authorize_user(allowed_roles: list[str]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user: User = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated"
                )
            print(current_user)
            if current_user.role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to perform this action"
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator