from datetime import datetime
from pydantic.types import UUID4
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from re import match

from app.schemas.product_schema import ProductSchemaRead


class CategorySchemaBase(BaseModel):
    """
    Classe que representa a base do esquema de categoria.
    """

    uuid: Optional[UUID4] = Field(None, description="The category's UUID.")
    name: str = Field(..., description="The category's name.")
    slug: str = Field(..., description="The category's slug.")

    created_at: Optional[datetime] = Field(
        None, description="The category's creation date."
    )
    updated_at: Optional[datetime] = Field(
        None, description="The category's last update date."
    )

    @field_validator("name")
    def validate_name(cls, value):
        # Nome da categoria deve conter apenas letras e no minimo 3 caracteres e no máximo 20
        if not match(r"^[a-zA-Z\s]{3,20}$", value):
            raise ValueError("Invalid category name.")

        return value

    @field_validator("slug")
    def validate_slug(cls, value):
        # O slug deve conter apenas letras minúsculas, traços e sublinhados
        if not match(r"^([a-z]|-|_)+$", value):
            raise ValueError("Invalid category slug.")

        return value


class CategorySchemaCreate(CategorySchemaBase):
    """
    Classe que representa o esquema de criação de categoria.
    """

    name: str = Field(..., description="The category's name.")
    slug: str = Field(..., description="The category's slug.")


class CategorySchemaUpdate(CategorySchemaBase):
    """
    Classe que representa o esquema de atualização de categoria.
    """

    name: Optional[str] = Field(None, description="The category's name.")
    slug: Optional[str] = Field(None, description="The category's slug.")


class CategorySchemaRead(CategorySchemaBase):
    """
    Classe que representa o esquema de leitura de categoria.
    """

    products: List[ProductSchemaRead] = Field(
        [], description="The category's products."
    )
