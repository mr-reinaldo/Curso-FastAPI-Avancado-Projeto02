from fastapi import status, HTTPException
from pytest import raises
from app.schemas.category_schema import (
    CategorySchemaCreate,
    CategorySchemaUpdate,
)

from app.schemas.responses import Message
from app.controllers.category_controller import CategoryController
from app.models.category_model import CategoryModel
from uuid import UUID
from typing import List


def test_get_all_categories(categories_on_db, db_session):
    """
    Teste de busca de todas as categorias
    """
    category_controller = CategoryController(db_session)

    response = category_controller.get_all()

    assert len(response) == len(categories_on_db)

    for category in response:
        assert category in categories_on_db


def test_get_category(categories_on_db, db_session):
    """
    Teste de busca de uma categoria
    """
    category_controller = CategoryController(db_session)

    category = categories_on_db[0]

    response = category_controller.get(category.uuid)

    assert response == category


def test_create_category(db_session):
    """
    Teste de criação de uma categoria
    """
    category_controller = CategoryController(db_session)

    category = CategorySchemaCreate(name="Nova categoria", slug="nova-categoria")

    response = category_controller.create(category)

    assert response.status == True
    assert response.message == "Category created successfully."

    db_session.delete(db_session.query(CategoryModel).first())
    db_session.commit()


def test_create_category_already_exists(categories_on_db, db_session):
    """
    Teste de criação de uma categoria que já existe
    """
    category_controller = CategoryController(db_session)

    category = CategorySchemaCreate(
        name=categories_on_db[0].name, slug="categoria-existente"
    )

    with raises(HTTPException) as exception:
        category_controller.create(category)

    assert exception.value.status_code == status.HTTP_409_CONFLICT
    assert exception.value.detail == "Category already exists."


def test_full_update_category(categories_on_db, db_session):
    """
    Teste de atualização completa de uma categoria
    """
    category_controller = CategoryController(db_session)

    category = categories_on_db[0]

    category_update = CategorySchemaUpdate(
        name="Categoria atualizada", slug="categoria-atualizada"
    )

    response = category_controller.full_update(
        category=category_update, uuid=category.uuid
    )

    assert response.status == True
    assert response.message == "Category updated successfully."


def test_partial_update_category(categories_on_db, db_session):
    """
    Teste de atualização parcial de uma categoria
    """
    category_controller = CategoryController(db_session)

    category = categories_on_db[0]

    category_update = CategorySchemaUpdate(name="Categoria atualizada")

    response = category_controller.partial_update(
        category=category_update, uuid=category.uuid
    )

    assert response.status == True
    assert response.message == "Category updated successfully."


def test_delete_category(db_session):
    """
    Teste de exclusão de uma categoria
    """
    category_controller = CategoryController(db_session)

    category = CategoryModel(name="Categoria teste", slug="categoria-teste")

    db_session.add(category)
    db_session.commit()

    response = category_controller.delete(category.uuid)

    assert response.status == True
    assert response.message == "Category deleted successfully."
