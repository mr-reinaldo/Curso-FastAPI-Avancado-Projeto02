from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from fastapi_pagination import Page, add_pagination
from app.core.deps import db_session, get_current_user
from app.models.product_model import ProductModel
from app.controllers.product_controller import ProductController
from app.schemas.product_schema import (
    ProductSchemaRead,
    ProductSchemaCreate,
    ProductSchemaUpdate,
)
from app.schemas.responses import Message
from uuid import UUID
from typing import Optional, List


router = APIRouter()


@router.get(
    "/products",
    response_model=Page[ProductSchemaRead],
    tags=["Products"],
    status_code=status.HTTP_200_OK,
)
def get_products(
    db: Session = Depends(db_session),
    current_user=Depends(get_current_user),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    """
    Retorna uma lista de produtos.
    """
    product_controller = ProductController(db)
    return product_controller.get_all(page=page, size=size)


@router.get(
    "/products/{uuid}",
    response_model=ProductSchemaRead,
    tags=["Products"],
    status_code=status.HTTP_200_OK,
)
def get_product(
    uuid: UUID,
    db: Session = Depends(db_session),
    current_user=Depends(get_current_user),
):
    """
    Retorna um produto.
    """
    product_controller = ProductController(db)
    return product_controller.get(uuid)


@router.post(
    "/products",
    response_model=Message,
    tags=["Products"],
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product: ProductSchemaCreate,
    db: Session = Depends(db_session),
    current_user=Depends(get_current_user),
):
    """
    Cria um produto.
    """
    product_controller = ProductController(db)
    return product_controller.create(product)


@router.put(
    "/products/{uuid}",
    response_model=Message,
    tags=["Products"],
    status_code=status.HTTP_200_OK,
)
def update_product(
    uuid: UUID,
    product: ProductSchemaUpdate,
    db: Session = Depends(db_session),
    current_user=Depends(get_current_user),
):
    """
    Atualiza um produto.
    """
    product_controller = ProductController(db)
    return product_controller.full_update(product, uuid)


@router.patch(
    "/products/{uuid}",
    response_model=Message,
    tags=["Products"],
    status_code=status.HTTP_200_OK,
)
def partial_update_product(
    uuid: UUID,
    product: ProductSchemaUpdate,
    db: Session = Depends(db_session),
    current_user=Depends(get_current_user),
):
    """
    Atualiza parcialmente um produto.
    """
    product_controller = ProductController(db)
    return product_controller.partial_update(product, uuid)


@router.delete(
    "/products/{uuid}",
    response_model=Message,
    tags=["Products"],
    status_code=status.HTTP_200_OK,
)
def delete_product(
    uuid: UUID,
    db: Session = Depends(db_session),
    current_user=Depends(get_current_user),
):
    """
    Deleta um produto.
    """
    product_controller = ProductController(db)
    return product_controller.delete(uuid)


# Adiciona paginação aos resultados
add_pagination(router)
