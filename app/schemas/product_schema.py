from datetime import datetime
from pydantic.types import UUID4
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from re import match


class ProductSchemaBase(BaseModel):
    """
    Classe que representa a base do esquema de produto.
    """

    uuid: Optional[UUID4] = Field(None, description="The product's UUID.")
    category_uuid: UUID4 = Field(..., description="The product's category UUID.")
    name: str = Field(..., description="The product's name.")
    slug: str = Field(..., description="The product's slug.")
    price: float = Field(..., description="The product's price.")
    stock: int = Field(..., description="The product's stock.")

    created_at: Optional[datetime] = Field(
        None, description="The product's creation date."
    )
    updated_at: Optional[datetime] = Field(
        None, description="The product's last update date."
    )

    @field_validator("name")
    def validate_name(cls, value):
        # Nome do produto deve conter apenas letras e no minimo 3 caracteres e no máximo 20 e pode conter espaços
        if not match(r"^[a-zA-Z0-9\s]{3,50}$", value):
            raise ValueError("Invalid product name.")

        return value

    @field_validator("slug")
    def validate_slug(cls, value):
        # O slug deve conter apenas letras minúsculas, traços e sublinhados
        if not match(r"^([a-z0-9]|-|_)+$", value):
            raise ValueError("Invalid product slug.")

        return value

    @field_validator("price")
    def validate_price(cls, value):
        # O preço do produto deve ser maior que zero
        if value <= 0:
            raise ValueError("Invalid product price.")

        return value

    @field_validator("stock")
    def validate_stock(cls, value):
        # O estoque do produto deve ser maior ou igual a zero
        if value < 0:
            raise ValueError("Invalid product stock.")

        return value


class ProductSchemaCreate(ProductSchemaBase):
    """
    Classe que representa o esquema de criação de produto.
    """

    name: str = Field(..., description="The product's name.")
    slug: str = Field(..., description="The product's slug.")
    price: float = Field(..., description="The product's price.")
    stock: int = Field(..., description="The product's stock.")
    category_uuid: UUID4 = Field(..., description="The product's category UUID.")


class ProductSchemaUpdate(ProductSchemaBase):
    """
    Classe que representa o esquema de atualização de produto.
    """

    name: Optional[str] = Field(None, description="The product's name.")
    slug: Optional[str] = Field(None, description="The product's slug.")
    price: Optional[float] = Field(None, description="The product's price.")
    stock: Optional[int] = Field(None, description="The product's stock.")
    category_uuid: Optional[UUID4] = Field(
        None, description="The product's category UUID."
    )


class ProductSchemaRead(ProductSchemaBase):
    """
    Classe que representa o esquema de leitura de produto.
    """

    pass
