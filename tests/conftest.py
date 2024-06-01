from faker import Faker
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

# Instância do Faker
fake = Faker(config={"locale": "pt_BR"}, use_weighting=True)


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
    category = {}

    # Nome da categoria deve conter apenas letras e no minimo 3 caracteres e no máximo 20
    # O slug deve conter apenas letras minúsculas, traços e sublinhados
    category["uuid"] = uuid4()
    category["name"] = fake.pystr(min_chars=3, max_chars=20)
    category["slug"] = fake.slug()
    category["created_at"] = datetime.now()
    category["updated_at"] = datetime.now()

    return category


@fixture
def generate_fake_user():
    """
    Função que gera um objeto fake de usuário.

    Returns:
        dict: Um objeto fake de usuário.
    """
    return {
        "uuid": uuid4(),
        "username": "userTest",
        "email": fake.email(),
        "password": fake.password(length=8, special_chars=True, digits=True),
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
        "uuid": uuid4(),
        "category_uuid": uuid4(),
        "name": fake.pystr(min_chars=3, max_chars=20),
        "slug": fake.slug(),
        "price": fake.pyfloat(
            left_digits=3, right_digits=2, positive=True, min_value=100, max_value=1000
        ),
        "stock": fake.pyint(min_value=1, max_value=200),
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
        username="TestUser",
        email="testuser@email.com",
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
    Função que cria usuários no banco de dados.

    Args:
        db_session (Session): Uma sessão de banco de dados.

    Returns:
        list: Uma lista de usuários.
    """
    users = []

    for _ in range(4):
        user = UserModel(  # substituir numeros por letras
            username=fake.first_name(),
            email=fake.email(),
            password=security.get_password_hash(
                fake.password(length=8, special_chars=True, digits=True)
            ),
        )
        users.append(user)

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
    Função que cria categorias no banco de dados.

    Args:
        db_session (Session): Uma sessão de banco de dados.

    Returns:
        list: Uma lista de categorias.
    """
    categories = []

    for _ in range(4):
        category = CategoryModel(
            name=fake.word(),
            slug=fake.slug(),
        )
        categories.append(category)

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
    Função que cria produtos no banco de dados.

    Args:
        db_session (Session): Uma sessão de banco de dados.
        categories_on_db (list): Uma lista de categorias.

    Returns:
        list: Uma lista de produtos.
    """
    products = []

    for _ in range(4):
        product = ProductModel(
            category_uuid=categories_on_db[0].uuid,
            name=fake.word(),
            slug=fake.slug(),
            price=fake.pyfloat(
                left_digits=3,
                right_digits=2,
                positive=True,
                min_value=100,
                max_value=1000,
            ),
            stock=fake.pyint(min_value=1, max_value=200),
        )
        products.append(product)

    for product in products:
        db_session.add(product)

    db_session.commit()

    for product in products:
        db_session.refresh(product)

    yield products

    for product in products:
        db_session.delete(product)

    db_session.commit()
