from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from pydantic.types import UUID4
from re import match
from datetime import datetime


class UserSchemaBase(BaseModel):

    model_config: ConfigDict = {
        "from_attributes": True,
    }

    uuid: Optional[UUID4] = Field(None, description="The user's UUID.")
    username: str = Field(..., description="The user's username.")
    email: EmailStr = Field(..., description="The user's email.")
    created_at: Optional[datetime] = Field(
        None, description="The user's creation date."
    )
    updated_at: Optional[datetime] = Field(
        None, description="The user's last update date."
    )

    @field_validator("username")
    def validate_username(cls, value):
        # Nome de usuário deve conter apenas letras e no minimo 3 caracteres e no máximo 20
        if not match(r"^[a-zA-Z]{3,20}$", value):
            raise ValueError("Invalid username.")

        return value


class UserSchemaCreate(UserSchemaBase):
    password: str = Field(..., description="The user's password.")

    @field_validator("password")
    def validate_password(cls, value):
        # Senha deve conter no mínimo 8 caracteres
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters.")

        return value


class UserSchemaUpdate(UserSchemaBase):
    username: Optional[str] = Field(None, description="The user's username.")
    email: Optional[EmailStr] = Field(None, description="The user's email.")
    password: Optional[str] = Field(None, description="The user's password.")

    @field_validator("username")
    def validate_username(cls, value):
        # Nome de usuário deve conter apenas letras e no minimo 3 caracteres e no máximo 20
        if not match(r"^[a-zA-Z]{3,20}$", value):
            raise ValueError("Invalid username.")

        return value

    @field_validator("password")
    def validate_password(cls, value):
        # Senha deve conter no mínimo 8 caracteres
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters.")

        return value


class UserSchemaLogin(BaseModel):
    email: EmailStr = Field(..., description="The user's email.")
    password: str = Field(..., description="The user's password.")
