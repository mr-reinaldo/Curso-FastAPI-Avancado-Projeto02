from pytest import raises
from pydantic import ValidationError
from app.schemas.category_schema import (
    CategorySchemaCreate,
    CategorySchemaUpdate,
    CategorySchemaRead,
)
from uuid import UUID
from datetime import datetime


def test_category_schema_create(generate_fake_category):
    """
    Teste de criação de um objeto CategorySchemaCreate

    Testes de sucesso:
    - Todos os campos obrigatórios e opcionais estão presentes
    """
    # Criação de um objeto CategorySchemaCreate
    category = CategorySchemaCreate(**generate_fake_category)

    # Testando se os campos estão corretos no objeto criado
    assert category.uuid == generate_fake_category["uuid"]
    assert category.name == generate_fake_category["name"]
    assert category.slug == generate_fake_category["slug"]
    assert category.created_at == generate_fake_category["created_at"]
    assert category.updated_at == generate_fake_category["updated_at"]

    # Testando se category é uma instância de CategorySchemaCreate
    assert isinstance(category, CategorySchemaCreate)

    # Testes os tipos dos campos do objeto criado
    assert isinstance(category.uuid, UUID)
    assert isinstance(category.name, str)
    assert isinstance(category.slug, str)
    assert isinstance(category.created_at, datetime)
    assert isinstance(category.updated_at, datetime)


def test_category_schema_create_error():
    """
    Teste de validação de campos obrigatórios no schema CategorySchemaCreate

    Testes de falha:
    - Todos os campos obrigatórios estão ausentes
    - name com menos de 3 caracteres
    - slug inválido
    """
    with raises(ValidationError):
        CategorySchemaCreate(**{})
    with raises(ValidationError):
        CategorySchemaCreate(**{"name": "te"})
    with raises(ValidationError):
        CategorySchemaCreate(**{"slug": "te_st"})
    with raises(ValidationError):
        CategorySchemaCreate(**{"name": 1, "slug": 1})


def test_category_schema_update(generate_fake_category):
    """
    Teste de criação de um objeto CategorySchemaUpdate

    Testes de sucesso:
    - Todos os campos obrigatórios e opcionais estão presentes
    """

    # Criação de um objeto CategorySchemaUpdate
    category = CategorySchemaUpdate(
        name=generate_fake_category["name"],
        slug=generate_fake_category["slug"],
    )

    # Print do objeto criado
    print(category)

    # Testes de sucesso
    assert isinstance(category, CategorySchemaUpdate)
    assert category.name == generate_fake_category["name"]
    assert category.slug == generate_fake_category["slug"]
    assert category.created_at is None
    assert category.updated_at is None


def test_category_schema_read(generate_fake_category):
    """
    Teste de criação de um objeto CategorySchemaRead

    Testes de sucesso:
    - Todos os campos obrigatórios e opcionais estão presentes
    """

    # Criação de um objeto CategorySchemaRead
    category = CategorySchemaRead(**generate_fake_category)

    # Testando se os campos estão corretos no objeto criado
    assert category.uuid == generate_fake_category["uuid"]
    assert category.name == generate_fake_category["name"]
    assert category.slug == generate_fake_category["slug"]
    assert category.created_at == generate_fake_category["created_at"]
    assert category.updated_at == generate_fake_category["updated_at"]

    # Testando se category é uma instância de CategorySchemaRead
    assert isinstance(category, CategorySchemaRead)

    # Testes os tipos dos campos do objeto criado
    assert isinstance(category.uuid, UUID)
    assert isinstance(category.name, str)
    assert isinstance(category.slug, str)
    assert isinstance(category.created_at, datetime)
    assert isinstance(category.updated_at, datetime)
