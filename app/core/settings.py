from typing import ClassVar
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from sqlalchemy.orm import declarative_base
from decouple import config as env_config


class Settings(BaseSettings):
    """
    Esta classe é responsável por gerenciar as configurações do aplicativo.
    """

    # Configurações do Pydantic
    model_config: ConfigDict = {
        "from_attributes": True,
    }
    # Encoding padrão das strings
    env_config.encoding = "utf-8"

    # Configurações do banco de dados
    DATABASE_URL: str = env_config("DATABASE_URL")
    DATABASE_BASE_MODEL: ClassVar = declarative_base()
    DATABASE_ECHO: bool = False
    DATABASE_ECHO_POOL: bool = False
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10

    # Configurações do JWT
    JWT_SECRET: str = env_config("JWT_SECRET")
    JWT_ALGORITHM: str = env_config("JWT_ALGORITHM")
    JWT_EXPIRATION: int = env_config("JWT_EXPIRATION", cast=int)

    # Configurações do FastAPI
    PREFIX: str = "/api/v1"
    TIMEZONE: str = env_config("TIMEZONE")


# Instanciando as configurações
settings = Settings()
