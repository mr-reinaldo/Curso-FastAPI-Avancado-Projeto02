from pydantic import BaseModel, Field
from typing import Optional


class Message(BaseModel):
    """
    Classe que representa uma mensagem.
    """

    status: Optional[bool] = Field(None, description="The status of the message.")
    message: Optional[str] = Field(None, description="The message.")


class JWTToken(BaseModel):
    """
    Classe que representa um token JWT.
    """

    access_token: Optional[str] = Field(None, description="The access token.")
    token_type: Optional[str] = Field(None, description="The token type.")
