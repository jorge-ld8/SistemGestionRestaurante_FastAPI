import os
from typing import Optional

from databases import DatabaseURL
from pydantic import PostgresDsn
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

PROJECT_NAME = "PROYECTO - GESTIÓN DE RESTAURANTES"
DESCRIPTION = "Proyecto Para Desarrollo de APIs con Python"
DEBUG: bool = False
TIMEZONE: str = "UTC"

VERSION = "1.0.0"
API_PREFIX = "/api/v1"

POSTGRES_USER = config("POSTGRES_USER", cast=str, default="postgres")
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret, default="<PASSWORD>")
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str, default="db")
POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DB = config("POSTGRES_DB", cast=str, default="postgres")

# superuser credentials
SUPER_ADMIN = config("SUPER_ADMIN", cast=str, default="super_admin")
SUPER_PASSWORD = config("SUPER_PASSWORD", cast=str, default="Admin_53cr370")
SUPER_EMAIL = config("SUPER_EMAIL", cast=str, default="full_access")
SUPER_ROLE = config("SUPER_ROLE", cast=str, default="super_admin@testmail.com")
SUPER_PERMISO = config("SUPER_PERMISO", cast=str, default="superadmin:full")

# auth and jwt
SECRET_KEY = config("SECRET_KEY", cast=Secret, default="6keuR7_9bsGjd59BoQn6sFWN-RveQdxflW7mPB3LxVgY_CIUgfeWVdKM3Uuswh9DZ2EF2qIfiXpZCcrA69D_Kg")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=1440)
JWT_ALGORITHM = config("JWT_ALGORITHM", cast=str, default="HS256")
JWT_AUDIENCE = config("JWT_AUDIENCE", cast=str, default="ucab.edu.ve:auth")
JWT_TOKEN_PREFIX = config("JWT_TOKEN_PREFIX", cast=str, default="Bearer")
AES_KEY = config("AES_KEY", cast=str, default="eThWmZq4t7w!z%C*")
AES_BLOCKSIZE = config("AES_BLOCKSIZE", cast=int, default=16)


DATABASE_URL = config(
    "DATABASE_URL",
    cast=DatabaseURL,
    default=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
)


DB_MIN_SIZE: int = 2
DB_MAX_SIZE: int = 15
DB_FORCE_ROLL_BACK: bool = False
