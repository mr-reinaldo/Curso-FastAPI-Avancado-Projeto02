from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import status
from fastapi.exceptions import HTTPException
from app.core.settings import settings
from app.core.security import security
from app.core.auth import create_access_token, authenticate_user
from app.models.user_model import UserModel
from app.schemas.user_schema import UserSchemaCreate, UserSchemaUpdate, UserSchemaLogin
from app.schemas.responses import Message, JWTToken
from datetime import datetime, timedelta, timezone
from uuid import UUID


class UserController:
    def __init__(self, db: Session):
        self.db = db

    def get(self, uuid: UUID) -> UserModel:

        user = self.db.query(UserModel).filter(UserModel.uuid == uuid).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        return user

    def get_all(self) -> list[UserModel]:

        users = self.db.query(UserModel).all()

        if not users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No users found.",
            )

        return users

    def create(self, user: UserSchemaCreate) -> Message:

        try:
            user.password = security.get_password_hash(user.password)
            user_model = UserModel(**user.model_dump())
            self.db.add(user_model)
            self.db.commit()
            self.db.refresh(user_model)
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

        user_model = self.db.query(UserModel).filter(UserModel.uuid == uuid).first()

        if not user_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        user_model.username = user.username
        user_model.email = user.email
        user_model.password = security.get_password_hash(user.password)
        user_model.updated_at = datetime.now(timezone.utc)

        self.db.commit()
        return Message(status=True, message="User updated successfully.")

    def partial_update(self, user: UserSchemaUpdate, uuid: UUID) -> Message:

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

        user_model.updated_at = datetime.now(timezone.utc)

        self.db.commit()
        return Message(status=True, message="User updated successfully.")

    def login(self, user: UserSchemaLogin) -> JWTToken:

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

        user = self.db.query(UserModel).filter(UserModel.uuid == uuid).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        self.db.delete(user)
        self.db.commit()
        return Message(status=True, message="User deleted successfully.")
