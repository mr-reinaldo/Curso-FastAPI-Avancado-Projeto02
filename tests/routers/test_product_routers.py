from fastapi.testclient import TestClient
from fastapi import status
from app.models.product_model import ProductModel
from app.core.settings import settings
from app.main import app

client = TestClient(app)


def test_create_product_router(get_token, categories_on_db, db_session):
    # Arrange
    product_data = {
        "name": "Test Product",
        "slug": "test-product",
        "price": 10.0,
        "stock": 10,
        "category_uuid": str(categories_on_db[0].uuid),
    }

    # Act
    response = client.post(
        f"{settings.PREFIX}/products",
        json=product_data,
        headers={"Authorization": f"Bearer {get_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["status"] == True
    assert response.json()["message"] == "Product created successfully."

    # Clean Up
    db_session.query(ProductModel).filter(ProductModel.name == "Test Product").delete()
    db_session.commit()


def test_create_product_router_existing_product(products_on_db, get_token):
    # Arrange
    product = products_on_db[0]
    product_data = {
        "name": product.name,
        "slug": product.slug,
        "price": product.price,
        "stock": product.stock,
        "category_uuid": str(product.category_uuid),
    }

    # Act
    response = client.post(
        f"{settings.PREFIX}/products",
        json=product_data,
        headers={"Authorization": f"Bearer {get_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "Product already exists."


def test_get_product_router(products_on_db, get_token):
    # Arrange
    product = products_on_db[0]

    # Act
    response = client.get(
        f"{settings.PREFIX}/products/{str(product.uuid)}",
        headers={"Authorization": f"Bearer {get_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == product.name
    assert response.json()["slug"] == product.slug
    assert response.json()["price"] == product.price
    assert response.json()["stock"] == product.stock
    assert response.json()["category_uuid"] == str(product.category_uuid)


def test_get_product_router_not_found(get_token):
    # Arrange
    uuid = "b0a8b4d1-0b8a-4c9f-8d3a-5d1b1b9d5e8e"

    # Act
    response = client.get(
        f"{settings.PREFIX}/products/{uuid}",
        headers={"Authorization": f"Bearer {get_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Product not found."


def test_get_all_products(products_on_db, get_token):
    # Act
    response = client.get(
        f"{settings.PREFIX}/products",
        headers={"Authorization": f"Bearer {get_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(products_on_db)


def test_full_upgrade_product_router(products_on_db, get_token):
    # Arrange
    product = products_on_db[0]
    product_data = {
        "name": "Updated Product",
        "slug": "updated-product",
        "price": 20.0,
        "stock": 20,
        "category_uuid": str(product.category_uuid),
    }

    # Act
    response = client.put(
        f"{settings.PREFIX}/products/{str(product.uuid)}",
        json=product_data,
        headers={"Authorization": f"Bearer {get_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == True
    assert response.json()["message"] == "Product updated successfully."


def test_partial_upgrade_product_router(products_on_db, get_token):
    # Arrange
    product = products_on_db[0]
    product_data = {
        "name": "Updated Product",
    }

    # Act
    response = client.patch(
        f"{settings.PREFIX}/products/{str(product.uuid)}",
        json=product_data,
        headers={"Authorization": f"Bearer {get_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == True
    assert response.json()["message"] == "Product updated successfully."


def test_delete_product_router(get_token, categories_on_db, db_session):
    # Arrange
    product = ProductModel(
        name="Test Product",
        slug="test-product",
        price=10.0,
        stock=10,
        category_uuid=categories_on_db[0].uuid,
    )

    db_session.add(product)
    db_session.commit()

    # Act
    response = client.delete(
        f"{settings.PREFIX}/products/{str(product.uuid)}",
        headers={"Authorization": f"Bearer {get_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == True
    assert response.json()["message"] == "Product deleted successfully."
