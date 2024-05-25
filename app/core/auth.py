from typing import Optional
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from pydantic import EmailStr
from app.core.settings import settings
from app.core.security import security
from app.models.user_model import UserModel

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.PREFIX}/login")


def authenticate_user(
    email: EmailStr, password: str, db: Session
) -> Optional[UserModel]:
    """
    Esta função é responsável por autenticar um usuário.

    Ela recebe um e-mail e uma senha, e usa essas credenciais para buscar um usuário no banco de dados.
    Se um usuário com o e-mail fornecido é encontrado, a função verifica se a senha fornecida corresponde à senha do usuário.
    Se a senha estiver correta, a função retorna o usuário. Caso contrário, ela retorna None.

    Parâmetros:
        email (EmailStr): O e-mail do usuário a ser autenticado.
        password (str): A senha do usuário a ser autenticada.
        db (Session): A sessão do banco de dados a ser usada para a consulta.

    Retorna:
        UserModel: O usuário autenticado, se a autenticação for bem-sucedida. Caso contrário, None.
    """

    user = (
        db.execute(select(UserModel).filter(UserModel.email == email)).scalars().first()
    )
    if not user:
        return None
    if not security.verify_password(password, user.password):
        return None
    return user


def _create_token(type_token: str, lifetime: timedelta, sub: str) -> str:
    """
    Esta função é responsável por criar um token JWT.

    Ela recebe um tipo de token, um tempo de vida e um assunto, e usa essas informações para criar um token JWT.

    Parâmetros:
        type_token (str): O tipo do token a ser criado.
        lifetime (timedelta): O tempo de vida do token.
        sub (str): O assunto do token.

    Retorna:
        str: O token JWT codificado.

    """

    expire = datetime.now(timezone.utc) + lifetime

    payload = {
        "type": type_token,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "sub": str(sub),
    }

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_access_token(sub: str) -> str:
    """
    Esta função é responsável por criar um token de acesso JWT.

    Ela recebe um assunto e usa essa informação, juntamente com as configurações predefinidas, para criar um token de acesso JWT.

    Parâmetros:
        sub (str): O assunto do token.

    Retorna:
        str: O token de acesso JWT codificado.
    """
    return _create_token(
        type_token="access_token",
        lifetime=timedelta(minutes=settings.JWT_EXPIRATION),
        sub=sub,
    )
