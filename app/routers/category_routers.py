from fastapi import APIRouter, Depends, status, Query
from fastapi_pagination import Page, add_pagination
from sqlalchemy.orm import Session
from app.core.deps import db_session, get_current_user
from app.controllers.category_controller import CategoryController
from app.schemas.category_schema import (
    CategorySchemaRead,
    CategorySchemaCreate,
    CategorySchemaUpdate,
)
from app.schemas.responses import Message
from uuid import UUID
from typing import List


router = APIRouter()


@router.get(
    "/categories",
    response_model=Page[CategorySchemaRead],
    tags=["Categories"],
    status_code=status.HTTP_200_OK,
)
def get_categories(
    db: Session = Depends(db_session),
    current_user=Depends(get_current_user),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    """
    Retorna uma lista de categorias.
    """
    category_controller = CategoryController(db)
    return category_controller.get_all(page, size)


@router.get(
    "/categories/{uuid}",
    response_model=CategorySchemaRead,
    tags=["Categories"],
    status_code=status.HTTP_200_OK,
)
def get_category(
    uuid: UUID,
    db: Session = Depends(db_session),
    current_user=Depends(get_current_user),
):
    """
    Retorna uma categoria.
    """
    category_controller = CategoryController(db)
    return category_controller.get(uuid)


@router.post(
    "/categories",
    response_model=Message,
    tags=["Categories"],
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    category: CategorySchemaCreate,
    db: Session = Depends(db_session),
    current_user=Depends(get_current_user),
):
    """
    Cria uma categoria.
    """
    category_controller = CategoryController(db)
    return category_controller.create(category)


@router.put(
    "/categories/{uuid}",
    response_model=Message,
    tags=["Categories"],
    status_code=status.HTTP_200_OK,
)
def update_category(
    uuid: UUID,
    category: CategorySchemaUpdate,
    db: Session = Depends(db_session),
    current_user=Depends(get_current_user),
):
    """
    Atualiza uma categoria.
    """
    category_controller = CategoryController(db)
    return category_controller.full_update(category, uuid)


@router.patch(
    "/categories/{uuid}",
    response_model=Message,
    tags=["Categories"],
    status_code=status.HTTP_200_OK,
)
def partial_update_category(
    uuid: UUID,
    category: CategorySchemaUpdate,
    db: Session = Depends(db_session),
    current_user=Depends(get_current_user),
):
    """
    Atualiza parcialmente uma categoria.
    """
    category_controller = CategoryController(db)
    return category_controller.partial_update(category, uuid)


@router.delete(
    "/categories/{uuid}",
    response_model=Message,
    tags=["Categories"],
    status_code=status.HTTP_200_OK,
)
def delete_category(
    uuid: UUID,
    db: Session = Depends(db_session),
    current_user=Depends(get_current_user),
):
    """
    Deleta uma categoria.
    """
    category_controller = CategoryController(db)
    return category_controller.delete(uuid)


# Adiciona paginação aos endpoints
add_pagination(router)
