from typing import ClassVar
from pydantic_settings import BaseSettings
from sqlalchemy.orm import declarative_base
from decouple import config as env_config


class Settings(BaseSettings):
    """
    Esta classe é responsável por gerenciar as configurações do aplicativo.
    """

    # Encoding padrão das strings
    env_config.encoding = "utf-8"

    # Configurações do banco de dados
    DATABASE_URL: str = env_config("DATABASE_URL")
    DATABASE_BASE_MODEL: ClassVar = declarative_base()

    # Configurações do JWT
    JWT_SECRET: str = env_config("JWT_SECRET")
    JWT_ALGORITHM: str = env_config("JWT_ALGORITHM")
    JWT_EXPIRATION: int = env_config


# Instanciando as configurações
settings = Settings()
