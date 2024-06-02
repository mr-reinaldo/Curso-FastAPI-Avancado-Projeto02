from fastapi.testclient import TestClient
from fastapi import status
from app.models.user_model import UserModel
from app.core.settings import settings
from app.main import app


client = TestClient(app)


def test_create_user_router(db_session):
    body = {
        "username": "TestUser",
        "email": "test@email.com",
        "password": "testpassword",
    }

    response = client.post(f"{settings.PREFIX}/users", json=body)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"status": True, "message": "User created successfully."}

    db_session.query(UserModel).filter(UserModel.username == "TestUser").delete()
    db_session.commit()


def test_create_user_router_existing_user(users_on_db):
    body = {
        "username": f"{users_on_db[0].username}",
        "email": f"{users_on_db[0].email}",
        "password": "testpassword",
    }

    response = client.post(f"{settings.PREFIX}/users", json=body)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {"detail": "User already exists."}


def test_get_user_router(users_on_db, get_token):
    response = client.get(
        f"{settings.PREFIX}/users/{users_on_db[0].uuid}",
        headers={"Authorization": f"Bearer {get_token}"},
    )

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["uuid"] == str(users_on_db[0].uuid)
    assert data["username"] == users_on_db[0].username
    assert data["email"] == users_on_db[0].email


def test_get_all_users_router(users_on_db, get_token):
    response = client.get(
        f"{settings.PREFIX}/users",
        headers={"Authorization": f"Bearer {get_token}"},
    )

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data.get("total") == len(users_on_db) + 1
    assert len(data.get("items")) == len(users_on_db) + 1


def test_full_update_user_router(users_on_db, get_token):
    body = {
        "username": "TestUser",
        "email": "teste@email.com",
        "password": "testpassword",
    }

    response = client.put(
        f"{settings.PREFIX}/users/{users_on_db[2].uuid}",
        json=body,
        headers={"Authorization": f"Bearer {get_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": True, "message": "User updated successfully."}


def test_partial_update_user_router(users_on_db, get_token):
    body = {"username": "TestUser"}

    response = client.patch(
        f"{settings.PREFIX}/users/{users_on_db[2].uuid}",
        json=body,
        headers={"Authorization": f"Bearer {get_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": True, "message": "User updated successfully."}


def test_delete_user_router(db_session, get_token):
    user = UserModel(
        username="teste",
        email="user@teste.com",
        password="password",
    )

    db_session.add(user)
    db_session.commit()

    response = client.delete(
        f"{settings.PREFIX}/users/{user.uuid}",
        headers={"Authorization": f"Bearer {get_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": True, "message": "User deleted successfully."}
