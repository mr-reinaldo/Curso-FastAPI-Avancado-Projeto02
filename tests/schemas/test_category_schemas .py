from pytest import raises
from pydantic import ValidationError
from app.schemas.user_schema import UserSchemaCreate, UserSchemaUpdate, UserSchemaLogin
from faker import Faker
from datetime import datetime
from uuid import uuid4

# Instância do Faker
fake = Faker()

# Criação de um objeto Faker
fake_user = {
    "uuid": uuid4(),
    "username": fake.name(),
    "email": fake.email(),
    "password": fake.password(length=8, special_chars=True, digits=True),
    "created_at": datetime.now(),
    "updated_at": datetime.now(),
}


def test_user_schema_create():
    """
    Teste de criação de um objeto UserSchemaCreate

    Testes de sucesso:
    - Todos os campos obrigatórios e opcionais estão presentes

    """

    # Criação de um objeto UserSchemaCreate
    user = UserSchemaCreate(**fake_user)

    # Print do objeto criado
    print(user)

    # Testes de sucesso
    assert user.uuid == fake_user["uuid"]
    assert user.username == fake_user["username"]
    assert user.email == fake_user["email"]
    assert user.password == fake_user["password"]
    assert user.created_at == fake_user["created_at"]
    assert user.updated_at == fake_user["updated_at"]


def test_user_schema_create_error():
    """
    Teste de validação de campos obrigatórios no schema UserSchemaCreate

    Testes de falha:
    - Todos os campos obrigatórios estão ausentes
    - username com menos de 3 caracteres
    - email inválido
    - password está presente, mas com menos de 8 caracteres
    """
    with raises(ValidationError):
        UserSchemaCreate(**{})
    with raises(ValidationError):
        UserSchemaCreate(**{"username": "te"})
    with raises(ValidationError):
        UserSchemaCreate(**{"email": "test"})
    with raises(ValidationError):
        UserSchemaCreate(**{"password": "test"})


def test_user_schema_update():
    """
    Teste de criação de um objeto UserSchemaUpdate

    Testes de sucesso:
    - Todos os campos obrigatórios e opcionais estão presentes

    """

    # Criação de um objeto UserSchemaUpdate
    user = UserSchemaUpdate(
        username=fake_user["username"],
        email=fake_user["email"],
        password=fake_user["password"],
    )

    # Print do objeto criado
    print(user)

    # Testes de sucesso
    assert user.username == fake_user["username"]
    assert user.email == fake_user["email"]
    assert user.password == fake_user["password"]


def test_user_schema_update_error():
    """
    Teste de validação de campos obrigatórios no schema UserSchemaUpdate

    Testes de falha:
    - Todos os campos obrigatórios estão ausentes
    - username com menos de 3 caracteres
    - email inválido
    - password está presente, mas com menos de 8 caracteres
    """
    with raises(ValidationError):
        UserSchemaUpdate(**{"username": "te"})
    with raises(ValidationError):
        UserSchemaUpdate(**{"email": "test"})
    with raises(ValidationError):
        UserSchemaUpdate(**{"password": "test"})


def test_user_schema_login():
    """
    Teste de criação de um objeto UserSchemaLogin

    Testes de sucesso:
    - Todos os campos obrigatórios e opcionais estão presentes

    """

    # Criação de um objeto UserSchemaLogin
    user = UserSchemaLogin(email=fake_user["email"], password=fake_user["password"])

    # Print do objeto criado
    print(user)

    # Testes de sucesso
    assert user.email == fake_user["email"]
    assert user.password == fake_user["password"]


def test_user_schema_login_error():
    """
    Teste de validação de campos obrigatórios no schema UserSchemaLogin

    Testes de falha:
    - Todos os campos obrigatórios estão ausentes
    - email inválido
    - password está presente, mas com menos de 8 caracteres
    """
    with raises(ValidationError):
        UserSchemaLogin(**{})
    with raises(ValidationError):
        UserSchemaLogin(**{"email": "test"})
    with raises(ValidationError):
        UserSchemaLogin(**{"password": "test"})
