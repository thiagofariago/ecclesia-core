"""
Schemas para autenticação.
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class Login(BaseModel):
    """Schema para login."""
    email: EmailStr = Field(..., description="Email do usuário")
    senha: str = Field(..., description="Senha do usuário")


class Token(BaseModel):
    """Schema de resposta de token."""
    access_token: str = Field(..., description="Token JWT de acesso")
    token_type: str = Field(default="bearer", description="Tipo do token")


class TokenData(BaseModel):
    """Schema de dados contidos no token."""
    email: Optional[str] = None
    user_id: Optional[int] = None
