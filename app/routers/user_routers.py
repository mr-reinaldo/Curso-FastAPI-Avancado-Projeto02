from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.controllers.user_controller import UserController
from app.core.deps import db_session, get_current_user
from app.schemas.user_schema import (
    UserSchemaCreate,
    UserSchemaLogin,
    UserSchemaUpdate,
    UserSchemaBase,
)
from app.schemas.responses import Message, JWTToken
from uuid import UUID
from typing import Optional, List

router = APIRouter()


@router.get("/users", response_model=List[UserSchemaBase], tags=["Users"])
def get_users(
    db: Session = Depends(db_session), current_user=Depends(get_current_user)
):
    """
    Retorna uma lista de usuários.
    """
    user_controller = UserController(db)
    return user_controller.get_all()


@router.get("/users/{uuid}", response_model=UserSchemaBase, tags=["Users"])
def get_user(
    uuid: UUID,
    db: Session = Depends(db_session),
    current_user=Depends(get_current_user),
):
    """
    Retorna um usuário.
    """
    user_controller = UserController(db)
    return user_controller.get(uuid)


@router.post(
    "/users",
    response_model=Message,
    tags=["Users"],
    status_code=status.HTTP_201_CREATED,
)
def create_user(user: UserSchemaCreate, db: Session = Depends(db_session)):
    """
    Cria um novo usuário.
    """
    user_controller = UserController(db)
    return user_controller.create(user)


@router.put(
    "/users/{uuid}",
    response_model=Message,
    tags=["Users"],
    status_code=status.HTTP_200_OK,
)
def full_update_user(
    uuid: UUID,
    user: UserSchemaUpdate,
    db: Session = Depends(db_session),
    current_user=Depends(get_current_user),
):
    """
    Atualiza um usuário.
    """
    user_controller = UserController(db)
    return user_controller.full_update(user, uuid)


@router.patch(
    "/users/{uuid}",
    response_model=Message,
    tags=["Users"],
    status_code=status.HTTP_200_OK,
)
def update_partial_user(
    uuid: UUID,
    user: UserSchemaUpdate,
    db: Session = Depends(db_session),
    current_user=Depends(get_current_user),
):
    """
    Atualiza um usuário.
    """
    user_controller = UserController(db)
    return user_controller.partial_update(user, uuid)


@router.post("/login", response_model=JWTToken, tags=["Users Auth"])
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db_session)
):
    """
    Autentica um usuário.
    """
    user_controller = UserController(db)
    user = UserSchemaLogin(email=form_data.username, password=form_data.password)
    return user_controller.login(user)


@router.delete(
    "/users/{uuid}",
    response_model=Message,
    tags=["Users"],
    status_code=status.HTTP_200_OK,
)
def delete_user(
    uuid: UUID,
    db: Session = Depends(db_session),
    current_user=Depends(get_current_user),
):
    """
    Deleta um usuário.
    """
    user_controller = UserController(db)
    return user_controller.delete(uuid)
