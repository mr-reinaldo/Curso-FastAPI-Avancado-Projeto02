from typing import Generator, Dict
from sqlalchemy.orm import Session

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from app.core.database import SessionLocal
from app.core.settings import settings
from app.core.auth import oauth2_scheme
from app.schemas.token_schema import TokenData
from app.models.user_model import UserModel


def db_session() -> Generator:
    """
    Dependencia para obter uma sessão do banco de dados.

    Returns:
        SessionLocal: Sessão do banco de dados

    """

    # Cria uma sessão do banco de dados
    db = SessionLocal()
    try:
        # Retorna a sessão do banco de dados (yield é como um return, mas não finaliza a função)
        yield db
    finally:
        # Fecha a sessão do banco de dados
        db.close()


def get_current_user(
    db: Session = Depends(db_session), token: str = Depends(oauth2_scheme)
) -> UserModel:
    """
    Dependencia para obter o usuário atual.

    Args:
        db (Session, optional): Sessão do banco de dados. Defaults to Depends(db_session).
        token (str, optional): Token de autenticação. Defaults to Depends(oauth2_scheme).

    Returns:
        UserModel: Usuário atual

    """

    # Define uma exceção personalizada para problemas de credenciais
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,  # Código de status HTTP para "Não autorizado"
        detail="Could not validate credentials",  # Detalhe da mensagem de erro
        headers={"WWW-Authenticate": "Bearer"},  # Cabeçalho de autenticação exigido
    )

    try:
        # Tenta decodificar o token JWT fornecido
        payload: Dict = jwt.decode(
            token=token,  # O token JWT a ser decodificado
            key=settings.JWT_SECRET,  # A chave secreta usada para decodificar o token
            algorithms=[
                settings.JWT_ALGORITHM
            ],  # O algoritmo usado para decodificar o token
            options={
                "verify_aud": False
            },  # Não verifica o campo "aud" (audiência) do token
        )

        # Extrai o nome de usuário do payload do token
        username: str = payload.get("sub")

        # Se o nome de usuário não estiver presente, lança uma exceção
        if username is None:
            raise credentials_exception

        # Armazena os dados do token em uma instância da classe TokenData
        token_data: TokenData = TokenData(username=username)

    # Se ocorrer um erro durante a decodificação do token, lança uma exceção
    except JWTError:
        raise credentials_exception

    # Consulta o banco de dados para encontrar um usuário com o nome de usuário extraído do token
    user = db.query(UserModel).filter(UserModel.username == token_data.username).first()

    # Se nenhum usuário for encontrado, lança uma exceção
    if user is None:
        raise credentials_exception

    # Retorna o objeto do usuário
    return user
