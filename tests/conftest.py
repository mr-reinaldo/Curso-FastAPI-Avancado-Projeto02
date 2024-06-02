from datetime import datetime
from uuid import uuid4
from pytest import fixture
from app.core.database import SessionLocal
from app.models.category_model import CategoryModel
from app.models.product_model import ProductModel
from app.models.user_model import UserModel
from app.core.security import security
from app.controllers.user_controller import UserController
from app.schemas.user_schema import UserSchemaLogin
from secrets import token_urlsafe


@fixture
def db_session():
    """
    Função que cria uma sessão de banco de dados.

    Returns:
        Session: Uma sessão de banco de dados.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@fixture
def get_token(user_on_db, db_session):
    """
    Função que retorna um token de autenticação.

    Returns:
        str: Um token de autenticação.
    """

    email = user_on_db["email"]
    password = user_on_db["password"]

    # user = db_session.query(UserModel).filter(UserModel.email == email).first()

    user_schema = UserSchemaLogin(
        email=email,
        password=password,
    )

    user_controller = UserController(db_session)
    token = user_controller.login(user_schema)

    return token.access_token


@fixture
def generate_fake_category():
    """
    Função que gera um objeto fake de categoria.

    Returns:
        dict: Um objeto fake de categoria.
    """
    return {
        "uuid": str(uuid4()),
        "name": "Fake Category",
        "slug": "fake-category",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }


@fixture
def generate_fake_user():
    """
    Função que gera um objeto fake de usuário.

    Returns:
        dict: Um objeto fake de usuário.
    """
    return {
        "uuid": str(uuid4()),
        "username": "fakeruser",
        "email": "fakeuser@gmail.com",
        "password": "fakepassword",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }


@fixture
def generate_fake_product():
    """
    Função que gera um objeto fake de produto.

    Returns:
        dict: Um objeto fake de produto.
    """
    return {
        "uuid": str(uuid4()),
        "category_uuid": str(uuid4()),
        "name": "Fake Product",
        "slug": "fake-product",
        "price": 100.00,
        "stock": 10,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }


@fixture
def user_on_db(db_session):
    """
    Função que cria um usuário no banco de dados.

    Args:
        db_session (Session): Uma sessão de banco de dados.

    Returns:
        UserModel: Um usuário

    """
    password = token_urlsafe(20)

    user = UserModel(
        username="testeusername",
        email="testeuser@gmail.com",
        password=security.get_password_hash(password),
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    yield {"email": user.email, "password": password}

    db_session.delete(user)
    db_session.commit()


@fixture
def users_on_db(db_session):
    """
    Função que cria vários usuários no banco de dados.

    Args:
        db_session (Session): Uma sessão de banco de dados.

    Returns:
        list: Uma lista de usuários.

    """
    users = [
        UserModel(
            username="testeusername1",
            email="testeuser1@gmail.com",
            password=security.get_password_hash(token_urlsafe(20)),
        ),
        UserModel(
            username="testeusername2",
            email="testeuser2@gmail.com",
            password=security.get_password_hash(token_urlsafe(20)),
        ),
        UserModel(
            username="testeusername3",
            email="testeuser3@gmail.com",
            password=security.get_password_hash(token_urlsafe(20)),
        ),
        UserModel(
            username="testeusername4",
            email="testeuser4@gmail.com",
            password=security.get_password_hash(token_urlsafe(20)),
        ),
    ]

    for user in users:
        db_session.add(user)

    db_session.commit()

    for user in users:
        db_session.refresh(user)

    yield users

    for user in users:
        db_session.delete(user)

    db_session.commit()


@fixture
def categories_on_db(db_session):
    """
    Função que cria várias categorias no banco de dados.

    Args:
        db_session (Session): Uma sessão de banco de dados.

    Returns:
        list: Uma lista de categorias.

    """
    categories = [
        CategoryModel(
            name="Category 1",
            slug="category-1",
        ),
        CategoryModel(
            name="Category 2",
            slug="category-2",
        ),
        CategoryModel(
            name="Category 3",
            slug="category-3",
        ),
        CategoryModel(
            name="Category 4",
            slug="category-4",
        ),
    ]

    for category in categories:
        db_session.add(category)

    db_session.commit()

    for category in categories:
        db_session.refresh(category)

    yield categories

    for category in categories:
        db_session.delete(category)

    db_session.commit()


@fixture
def products_on_db(db_session, categories_on_db):
    """
    Função que cria vários produtos no banco de dados.

    Args:
        db_session (Session): Uma sessão de banco de dados.
        categories_on_db (list): Uma lista de categorias.

    Returns:
        list: Uma lista de produtos.

    """
    products = [
        ProductModel(
            category_uuid=categories_on_db[0].uuid,
            name="Product 1",
            slug="product-1",
            price=100.00,
            stock=10,
        ),
        ProductModel(
            category_uuid=categories_on_db[1].uuid,
            name="Product 2",
            slug="product-2",
            price=200.00,
            stock=20,
        ),
        ProductModel(
            category_uuid=categories_on_db[2].uuid,
            name="Product 3",
            slug="product-3",
            price=300.00,
            stock=30,
        ),
        ProductModel(
            category_uuid=categories_on_db[3].uuid,
            name="Product 4",
            slug="product-4",
            price=400.00,
            stock=40,
        ),
    ]

    for product in products:
        db_session.add(product)

    db_session.commit()

    for product in products:
        db_session.refresh(product)

    yield products

    for product in products:
        db_session.delete(product)

    db_session.commit()
