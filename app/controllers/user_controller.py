from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import status
from fastapi.exceptions import HTTPException
from app.core.security import security
from app.core.auth import create_access_token, authenticate_user
from fastapi_pagination import Params, Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.future import select
from app.models.user_model import UserModel
from app.schemas.user_schema import UserSchemaCreate, UserSchemaUpdate, UserSchemaLogin
from app.schemas.responses import Message, JWTToken
from datetime import datetime
from uuid import UUID


class UserController:
    def __init__(self, db: Session):
        self.db = db

    def get(self, uuid: UUID) -> UserModel:
        """
        Método para retornar um usuário.

        Parâmetros:
        - uuid: UUID (Identificador do usuário)

        Retorno:
        - UserModel (Usuário)
        """
        user = self.db.query(UserModel).filter(UserModel.uuid == uuid).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        return user

    def get_all(self, page: int = 1, size: int = 50) -> Page[UserModel]:
        """
        Método para retornar uma lista de usuários.

        Parâmetros:
        - page: int (Página atual)
        - size: int (Quantidade de registros por página)

        Retorno:
        - Page[UserModel] (Lista de usuários)
        """

        query = select(UserModel).order_by(UserModel.created_at.desc())
        params = Params(page=page, size=size)
        return paginate(self.db, query, params)

    def create(self, user: UserSchemaCreate) -> Message:
        """
        Método para criar um usuário.

        Parâmetros:
        - user: UserSchemaCreate (Usuário)

        Retorno:
        - Message (Mensagem de retorno)

        """

        try:
            user.password = security.get_password_hash(user.password)
            user_model = UserModel(**user.model_dump())
            self.db.add(user_model)
            self.db.commit()

            return Message(status=True, message="User created successfully.")
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists.",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {e}",
            )

    def full_update(self, user: UserSchemaUpdate, uuid: UUID) -> Message:
        """
        Método para atualizar um usuário.

        Parâmetros:
        - user: UserSchemaUpdate (Usuário)
        - uuid: UUID (Identificador do usuário)

        Retorno:
        - Message (Mensagem de retorno)

        """

        user_model = self.db.query(UserModel).filter(UserModel.uuid == uuid).first()

        if not user_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        user_model.username = user.username
        user_model.email = user.email
        user_model.password = security.get_password_hash(user.password)
        user_model.updated_at = datetime.now()

        self.db.commit()
        return Message(status=True, message="User updated successfully.")

    def partial_update(self, user: UserSchemaUpdate, uuid: UUID) -> Message:
        """
        Método para atualizar parcialmente um usuário.

        Parâmetros:
        - user: UserSchemaUpdate (Usuário)
        - uuid: UUID (Identificador do usuário)

        Retorno:
        - Message (Mensagem de retorno)

        """

        user_model = self.db.query(UserModel).filter(UserModel.uuid == uuid).first()

        if not user_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        if user.username:
            user_model.username = user.username
        if user.email:
            user_model.email = user.email
        if user.password:
            user_model.password = security.get_password_hash(user.password)

        user_model.updated_at = datetime.now()

        self.db.commit()
        return Message(status=True, message="User updated successfully.")

    def login(self, user: UserSchemaLogin) -> JWTToken:
        """
        Método para realizar login.

        Parâmetros:
        - user: UserSchemaLogin (Usuário)

        Retorno:
        - JWTToken (Token de autenticação)
        """

        user = authenticate_user(user.email, user.password, self.db)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
            )

        return JWTToken(
            access_token=create_access_token(user.username),
            token_type="bearer",
        )

    def delete(self, uuid: UUID) -> Message:
        """
        Método para deletar um usuário.

        Parâmetros:
        - uuid: UUID (Identificador do usuário)

        Retorno:
        - Message (Mensagem de retorno)

        """
        user = self.db.query(UserModel).filter(UserModel.uuid == uuid).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        self.db.delete(user)
        self.db.commit()
        return Message(status=True, message="User deleted successfully.")
