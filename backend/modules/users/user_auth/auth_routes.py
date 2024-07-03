from typing import List
from databases import Database
from fastapi import APIRouter, Body, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from modules.users.auths.auth_schemas import (
    AuthEmailRecoverPsw,
    AuthResetPsw,
    AuthResponse,
)
from modules.users.user_auth.auth_services import AuthService
from shared.core.db.db_dependencies import get_database
from shared.utils.service_result import ServiceResult, handle_result
from shared.core.db.db_connection import get_db

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.post("/login", name="auth:login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
    db: Database = Depends(get_db),
) -> ServiceResult:
    result = await AuthService().authenticate_user(
        username=form_data.username, password=form_data.password, db=db
    )

    return handle_result(result)


@router.get("/verify_token", name="auth:verify_token", status_code=status.HTTP_200_OK)
async def verify_token(
    token: str,
    db: Database = Depends(get_db),
) -> ServiceResult:

    result = await AuthService().verify_token(token=token, db=db)
    return handle_result(result)
