from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.controllers.user_controller import UserController
from app.core.deps import db_session
from app.schemas.user_schema import UserSchemaCreate, UserSchemaLogin
from app.schemas.responses import Message, JWTToken

router = APIRouter()


@router.post("/users", response_model=Message, tags=["Users"])
def create_user(user: UserSchemaCreate, db: Session = Depends(db_session)):
    """
    Cria um novo usuário.
    """
    user_controller = UserController(db)
    return user_controller.create(user)


@router.post("/login", response_model=JWTToken, tags=["Users"])
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db_session)
):
    """
    Autentica um usuário.
    """
    user_controller = UserController(db)
    user = UserSchemaLogin(email=form_data.username, password=form_data.password)
    return user_controller.login(user)
