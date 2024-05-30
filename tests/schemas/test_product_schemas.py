from pytest import raises
from pydantic import ValidationError
from app.schemas.product_schema import (
    ProductSchemaCreate,
    ProductSchemaUpdate,
    ProductSchemaRead,
)
from uuid import UUID
from datetime import datetime


def test_product_schema_create(generate_fake_product):
    """
    Teste de criação de um objeto ProductSchemaCreate

    Testes de sucesso:
    - Todos os campos obrigatórios e opcionais estão presentes
    """
    # Criação de um objeto ProductSchemaCreate
    product = ProductSchemaCreate(**generate_fake_product)

    # Testando se os campos estão corretos no objeto criado
    assert product.uuid == generate_fake_product["uuid"]
    assert product.category_uuid == generate_fake_product["category_uuid"]
    assert product.name == generate_fake_product["name"]
    assert product.slug == generate_fake_product["slug"]
    assert product.price == generate_fake_product["price"]
    assert product.stock == generate_fake_product["stock"]
    assert product.created_at == generate_fake_product["created_at"]
    assert product.updated_at == generate_fake_product["updated_at"]

    # Testando se product é uma instância de ProductSchemaCreate
    assert isinstance(product, ProductSchemaCreate)

    # Testes os tipos dos campos do objeto criado
    assert isinstance(product.uuid, UUID)
    assert isinstance(product.category_uuid, UUID)
    assert isinstance(product.name, str)
    assert isinstance(product.slug, str)
    assert isinstance(product.price, float)
    assert isinstance(product.stock, int)
    assert isinstance(product.created_at, datetime)
    assert isinstance(product.updated_at, datetime)


def test_product_schema_create_missing_required_fields(generate_fake_product):
    """
    Teste de criação de um objeto ProductSchemaCreate

    Testes de falha:
    - Campos obrigatórios faltando
    """
    # Removendo os campos obrigatórios
    del generate_fake_product["name"]
    del generate_fake_product["slug"]

    # Testes de falha
    with raises(ValidationError):
        ProductSchemaCreate(**generate_fake_product)

    # Removendo os campos obrigatórios
    del generate_fake_product["category_uuid"]
    del generate_fake_product["price"]
    del generate_fake_product["stock"]

    # Testes de falha
    with raises(ValidationError):
        ProductSchemaCreate(**generate_fake_product)


def test_product_schema_update(generate_fake_product):
    """
    Teste de criação de um objeto ProductSchemaUpdate

    Testes de sucesso:
    - Todos os campos obrigatórios e opcionais estão presentes
    """

    # Criação de um objeto ProductSchemaUpdate
    product = ProductSchemaUpdate(
        category_uuid=generate_fake_product["category_uuid"],
        name=generate_fake_product["name"],
        slug=generate_fake_product["slug"],
        price=generate_fake_product["price"],
        stock=generate_fake_product["stock"],
    )

    # Print do objeto criado
    print(product)

    # Testes de sucesso

    assert product.category_uuid == generate_fake_product["category_uuid"]
    assert product.name == generate_fake_product["name"]
    assert product.slug == generate_fake_product["slug"]
    assert product.price == generate_fake_product["price"]
    assert product.stock == generate_fake_product["stock"]

    # Testando se product é uma instância de ProductSchemaUpdate
    assert isinstance(product, ProductSchemaUpdate)

    # Testes os tipos dos campos do objeto criado
    assert isinstance(product.category_uuid, UUID)
    assert isinstance(product.name, str)
    assert isinstance(product.slug, str)
    assert isinstance(product.price, float)
    assert isinstance(product.stock, int)

    # Testando se os campos created_at e updated_at são None
    assert product.created_at is None
    assert product.updated_at is None


def test_product_schema_read(generate_fake_product):
    """
    Teste de criação de um objeto ProductSchemaRead

    Testes de sucesso:
    - Todos os campos obrigatórios e opcionais estão presentes
    """

    # Criação de um objeto ProductSchemaRead
    product = ProductSchemaRead(**generate_fake_product)

    # Testando se os campos estão corretos no objeto criado
    assert product.uuid == generate_fake_product["uuid"]
    assert product.category_uuid == generate_fake_product["category_uuid"]
    assert product.name == generate_fake_product["name"]
    assert product.slug == generate_fake_product["slug"]
    assert product.price == generate_fake_product["price"]
    assert product.stock == generate_fake_product["stock"]
    assert product.created_at == generate_fake_product["created_at"]
    assert product.updated_at == generate_fake_product["updated_at"]

    # Testando se product é uma instância de ProductSchemaRead
    assert isinstance(product, ProductSchemaRead)

    # Testes os tipos dos campos do objeto criado
    assert isinstance(product.uuid, UUID)
    assert isinstance(product.category_uuid, UUID)
    assert isinstance(product.name, str)
    assert isinstance(product.slug, str)
    assert isinstance(product.price, float)
    assert isinstance(product.stock, int)
    assert isinstance(product.created_at, datetime)
    assert isinstance(product.updated_at, datetime)


def test_product_schema_read_missing_required_fields(generate_fake_product):
    """
    Teste de criação de um objeto ProductSchemaRead

    Testes de falha:
    - Campos obrigatórios faltando
    """
    # Removendo os campos obrigatórios
    del generate_fake_product["name"]
    del generate_fake_product["slug"]

    # Testes de falha
    with raises(ValidationError):
        ProductSchemaRead(**generate_fake_product)

    # Removendo os campos obrigatórios
    del generate_fake_product["category_uuid"]
    del generate_fake_product["price"]
    del generate_fake_product["stock"]

    # Testes de falha
    with raises(ValidationError):
        ProductSchemaRead(**generate_fake_product)
