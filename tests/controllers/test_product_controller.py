from fastapi import status, HTTPException
from pytest import raises
from app.schemas.product_schema import ProductSchemaCreate, ProductSchemaUpdate
from app.schemas.responses import Message
from app.controllers.product_controller import ProductController
from app.models.product_model import ProductModel
from uuid import UUID
from typing import List


def test_get_all_products(products_on_db, db_session):
    """
    Teste de busca de todos os produtos
    """
    product_controller = ProductController(db_session)

    response = product_controller.get_all()

    assert len(response) == len(products_on_db)

    for product in response:
        assert product in products_on_db


def test_get_product(products_on_db, db_session):
    """
    Teste de busca de um produto
    """
    product_controller = ProductController(db_session)

    product = products_on_db[0]

    response = product_controller.get(product.uuid)

    assert response == product


def test_create_product(categories_on_db, db_session):
    """
    Teste de criação de um produto
    """
    product_controller = ProductController(db_session)

    product = ProductSchemaCreate(
        category_uuid=categories_on_db[0].uuid,
        name="Product",
        slug="product",
        price=10.0,
        stock=10,
    )

    response = product_controller.create(product)

    assert response.status == True
    assert response.message == "Product created successfully."

    product_model = (
        db_session.query(ProductModel).filter(ProductModel.name == product.name).first()
    )

    assert product_model.name == product.name
    assert product_model.slug == product.slug
    assert product_model.price == product.price
    assert product_model.stock == product.stock

    db_session.delete(product_model)
    db_session.commit()


def test_create_product_already_exists(products_on_db, db_session):
    """
    Teste de criação de um produto que já existe
    """
    product_controller = ProductController(db_session)

    product = ProductSchemaCreate(
        category_uuid=products_on_db[0].category_uuid,
        name=products_on_db[0].name,
        slug="product",
        price=10.0,
        stock=10,
    )

    with raises(HTTPException) as exception:
        product_controller.create(product)

    assert exception.value.status_code == status.HTTP_409_CONFLICT
    assert exception.value.detail == "Product already exists."


def test_full_update_product(products_on_db, db_session):
    """
    Teste de atualização completa de um produto
    """
    product_controller = ProductController(db_session)

    product = products_on_db[0]

    product_update = ProductSchemaCreate(
        category_uuid=product.category_uuid,
        name="Product Update",
        slug="product-update",
        price=20.0,
        stock=20,
    )

    response = product_controller.full_update(product_update, product.uuid)

    assert response.status == True
    assert response.message == "Product updated successfully."

    product_model = (
        db_session.query(ProductModel).filter(ProductModel.uuid == product.uuid).first()
    )

    assert product_model.name == product_update.name
    assert product_model.slug == product_update.slug
    assert product_model.price == product_update.price
    assert product_model.stock == product_update.stock


def test_partial_update_product(products_on_db, db_session):
    """
    Teste de atualização parcial de um produto
    """
    product_controller = ProductController(db_session)

    product = products_on_db[0]

    product_update = ProductSchemaUpdate(name="Product Update")

    response = product_controller.partial_update(product_update, product.uuid)

    assert response.status == True
    assert response.message == "Product updated successfully."

    product_model = (
        db_session.query(ProductModel).filter(ProductModel.uuid == product.uuid).first()
    )

    assert product_model.name == product_update.name
    assert product_model.slug == product.slug
    assert product_model.price == product.price
    assert product_model.stock == product.stock


def test_delete_product(categories_on_db, db_session):
    """
    Teste de exclusão de um produto
    """
    product_controller = ProductController(db_session)

    product = ProductModel(
        category_uuid=categories_on_db[0].uuid,
        name="Product",
        slug="product",
        price=10.0,
        stock=10,
    )

    db_session.add(product)
    db_session.commit()

    response = product_controller.delete(product.uuid)

    assert response.status == True
    assert response.message == "Product deleted successfully."
