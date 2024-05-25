from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from app.core.settings import settings
from app.core.security import security
from app.core.auth import create_access_token, authenticate_user
from app.models.user_model import UserModel
from app.schemas.user_schema import UserSchemaCreate, UserSchemaUpdate, UserSchemaLogin
from app.schemas.responses import Message, JWTToken
from app.schemas.token_schema import TokenData
from datetime import datetime, timedelta, timezone


class UserController:
    def __init__(self, db: Session):
        self.db = db

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
