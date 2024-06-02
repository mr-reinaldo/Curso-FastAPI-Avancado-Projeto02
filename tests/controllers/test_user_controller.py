from app.schemas.user_schema import (
    UserSchemaCreate,
    UserSchemaUpdate,
    UserSchemaLogin,
)
from app.schemas.responses import JWTToken
from app.controllers.user_controller import UserController
from app.models.user_model import UserModel
from fastapi_pagination import Page


def test_get_all_users(users_on_db, db_session):
    """
    Teste de busca de todos os usuários
    """
    user_controller = UserController(db_session)

    response = user_controller.get_all(page=1, size=10)

    assert type(response) == Page
    assert len(response.items) == len(users_on_db)
    assert response.total == len(users_on_db)


def test_create_user(generate_fake_user, db_session):
    """
    Teste de criação de usuário
    """
    user_controller = UserController(db_session)

    fake_user = UserSchemaCreate(
        username=generate_fake_user["username"],
        email=generate_fake_user["email"],
        password=generate_fake_user["password"],
    )

    response = user_controller.create(fake_user)

    assert response.status == True
    assert response.message == "User created successfully."

    user_in_db = db_session.query(UserModel).all()

    assert len(user_in_db) == 1
    assert user_in_db[0].username == fake_user.username
    assert user_in_db[0].email == fake_user.email
    assert user_in_db[0].password == fake_user.password

    db_session.delete(user_in_db[0])
    db_session.commit()


def test_get_user_by_uuid(users_on_db, db_session):
    """
    Teste de busca de usuário por UUID
    """
    user_controller = UserController(db_session)

    for user in users_on_db:
        response = user_controller.get(user.uuid)
        assert response.uuid == user.uuid
        assert response.username == user.username
        assert response.email == user.email


def test_full_update_user(users_on_db, db_session):
    """
    Teste de atualização completa de usuário
    """

    user_controller = UserController(db_session)

    for user in users_on_db:
        fake_user = UserSchemaUpdate(
            username="newUsername",
            email=f"{user.username}@email.com".lower(),
            password="newPassword",
        )
        response = user_controller.full_update(user=fake_user, uuid=user.uuid)
        assert response.status == True
        assert response.message == "User updated successfully."


def test_partial_update_user(users_on_db, db_session):
    """
    Teste de atualização parcial de usuário
    """

    user_controller = UserController(db_session)

    for user in users_on_db:
        fake_user = UserSchemaUpdate(username="newUsername")
        response = user_controller.partial_update(user=fake_user, uuid=user.uuid)
        assert response.status == True
        assert response.message == "User updated successfully."


def test_delete_user(generate_fake_user, db_session):
    """
    Teste de deleção de usuário
    """

    user_controller = UserController(db_session)

    fake_user = UserSchemaCreate(
        username=generate_fake_user["username"],
        email=generate_fake_user["email"],
        password=generate_fake_user["password"],
    )

    response = user_controller.create(fake_user)

    assert response.status == True
    assert response.message == "User created successfully."

    user_in_db = db_session.query(UserModel).all()

    assert len(user_in_db) == 1

    response = user_controller.delete(user_in_db[0].uuid)

    assert response.status == True
    assert response.message == "User deleted successfully."


def test_login_user(user_on_db, db_session):
    """
    Teste de login de usuário
    """

    user_controller = UserController(db_session)

    fake_user = UserSchemaLogin(
        email=user_on_db["email"],
        password=user_on_db["password"],
    )

    response = user_controller.login(fake_user)

    assert response.access_token != None
    assert response.token_type == "bearer"
    assert isinstance(response, JWTToken)
    assert isinstance(response.access_token, str)
    assert isinstance(response.token_type, str)
    assert response.access_token != ""
    assert response.token_type != ""
