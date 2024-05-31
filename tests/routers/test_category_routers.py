from fastapi.testclient import TestClient
from fastapi import status
from app.models.category_model import CategoryModel
from app.core.settings import settings
from app.main import app


client = TestClient(app)


def test_create_category_router(get_token, db_session):
    # Arrange
    category_data = {
        "name": "Test Category",
        "slug": "test-category",
    }

    # Act
    response = client.post(
        f"{settings.PREFIX}/categories",
        json=category_data,
        headers={"Authorization": f"Bearer {get_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["status"] == True
    assert response.json()["message"] == "Category created successfully."

    # Clean Up
    db_session.query(CategoryModel).filter(
        CategoryModel.name == "Test Category"
    ).delete()
    db_session.commit()


def test_create_category_router_existing_category(categories_on_db, get_token):
    # Arrange
    category = categories_on_db[0]
    category_data = {
        "name": category.name,
        "slug": category.slug,
    }

    # Act
    response = client.post(
        f"{settings.PREFIX}/categories",
        json=category_data,
        headers={"Authorization": f"Bearer {get_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "Category already exists."


def test_get_category_router(categories_on_db, get_token):
    # Arrange
    category = categories_on_db[0]

    # Act
    response = client.get(
        f"{settings.PREFIX}/categories/{category.uuid}",
        headers={"Authorization": f"Bearer {get_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["uuid"] == str(category.uuid)
    assert response.json()["name"] == category.name
    assert response.json()["slug"] == category.slug


def test_get_all_categories(categories_on_db, get_token):
    # Act
    response = client.get(
        f"{settings.PREFIX}/categories",
        headers={"Authorization": f"Bearer {get_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(categories_on_db)


def test_full_upgrade_category_router(categories_on_db, get_token):
    # Arrange
    category = categories_on_db[0]
    category_data = {
        "name": "Updated Category",
        "slug": "updated-category",
    }

    # Act
    response = client.put(
        f"{settings.PREFIX}/categories/{category.uuid}",
        json=category_data,
        headers={"Authorization": f"Bearer {get_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == True
    assert response.json()["message"] == "Category updated successfully."


def test_partial_upgrade_category_router(categories_on_db, get_token):
    # Arrange
    category = categories_on_db[0]
    category_data = {
        "name": "Updated Category",
    }

    # Act
    response = client.patch(
        f"{settings.PREFIX}/categories/{category.uuid}",
        json=category_data,
        headers={"Authorization": f"Bearer {get_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == True
    assert response.json()["message"] == "Category updated successfully."


def test_delete_category_router(get_token, db_session):
    # Arrange
    category_data = {
        "name": "Test Category",
        "slug": "test-category",
    }

    db_session.add(CategoryModel(**category_data))
    db_session.commit()

    category = (
        db_session.query(CategoryModel)
        .filter(CategoryModel.name == "Test Category")
        .first()
    )

    # Act
    response = client.delete(
        f"{settings.PREFIX}/categories/{category.uuid}",
        headers={"Authorization": f"Bearer {get_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == True
    assert response.json()["message"] == "Category deleted successfully."
