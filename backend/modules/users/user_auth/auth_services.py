from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from databases import Database
from loguru import logger
from modules.users.auths.auth_exceptions import AuthExceptions
from modules.users.user_auth.auth_repositories import AuthRepository
from modules.users.user_auth.auth_schemas import (
    AccessToken,
    AuthEmailRecoverPsw,
    AuthResetPsw,
    AuthResponse,
    JWTCreds,
    JWTMeta,
    JWTPayload,
)
from passlib.context import CryptContext
from pydantic import ValidationError
from shared.core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_ALGORITHM,
    JWT_AUDIENCE,
    SECRET_KEY,
)

from shared.utils.service_result import ServiceResult

from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def verify_password(self, password: str, hashed_pw: str) -> bool:
        # return pwd_context.verify(password + salt, hashed_pw)
        return pwd_context.verify(password, hashed_pw)

    def create_access_token_for_user(
            self,
            *,
            user: User,
            secret_key: str = str(SECRET_KEY),
            audience: str = JWT_AUDIENCE,
            expires_in: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:

        if not user:
            return None

        creation_time = datetime.now().replace(tzinfo=None)
        expire_time = creation_time + timedelta(minutes=expires_in)

        jwt_meta = JWTMeta(
            aud=audience,
            iat=datetime.timestamp(creation_time),
            exp=datetime.timestamp(expire_time),
        )

        jwt_creds = JWTCreds(username=user.user_name)
        token_payload = JWTPayload(
            **jwt_meta.dict(),
            **jwt_creds.dict(),
        )
        access_token = jwt.encode(token_payload.dict(), secret_key, algorithm=JWT_ALGORITHM)
        return access_token

    async def authenticate_user(self, username: str, password: str, db: Database) -> ServiceResult:
        from shared.utils.crypto_credentials import CryptoAES

        if not username:
            logger.error("Try to login without username")
            return ServiceResult(AuthExceptions.AuthNoUsernameException())

        if not password:
            logger.error("Try to login without password")
            return ServiceResult(AuthExceptions.AuthNoPasswordException())

        user = await AuthRepository(db).authenticate_user(username=username, password=password)

        if not user:
            logger.error(f"Trying to login with invalid credentials, username: {username}")
            return ServiceResult(AuthExceptions.AuthNoValidCredencialsException())

        if not self.verify_password(password=password, hashed_pw=user.password):
            logger.error(f"Trying to login with invalid credentials, username: {username}")
            return ServiceResult(AuthExceptions.AuthNoValidCredencialsException())

        user_autenticated = AuthResponse(
            access_token=self.create_access_token_for_user(user=user),
            token_type="bearer",
            id=user.user_id,
            fullname=user.name,
            username=user.user_name,
            role=user.role,
            # permissions=user.permissions,
        )

        return ServiceResult(user_autenticated)


    async def verify_token(self, token: str, db: Database) -> ServiceResult:
        token_dict = await AuthRepository(db).get_token_by_value(token=token)

        if token_dict.get("token"):
            return ServiceResult(AuthExceptions.AuthRestPswTokenUsedException())

        return ServiceResult("token válido")

    def get_username_from_token(self, token: str, secret_key: str) -> str | None:
        try:
            decoded_token = jwt.decode(
                token,
                str(secret_key),
                audience=JWT_AUDIENCE,
                algorithms=[JWT_ALGORITHM],
            )
            payload = JWTPayload(**decoded_token)

        except (jwt.PyJWTError, ValidationError):
            raise AuthExceptions.AuthNoValidTokenCredentialsException()

        except jwt.ExpiredSignatureError:
            raise AuthExceptions.AuthTokenExpiredException()

        return payload.username

