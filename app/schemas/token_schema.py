from typing import Optional
from pydantic import BaseModel, Field


class TokenData(BaseModel):
    """
    Classe que representa os dados do token.
    """

    username: Optional[str] = Field(None, title="Nome de usuário")
