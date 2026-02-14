"""
Schemas para Usuário.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.models.usuario import RoleEnum


class UsuarioBase(BaseModel):
    """Schema base de Usuário."""
    nome: str = Field(..., min_length=1, max_length=255, description="Nome do usuário")
    email: EmailStr = Field(..., description="Email do usuário")
    role: RoleEnum = Field(default=RoleEnum.OPERADOR, description="Papel do usuário no sistema")
    ativo: bool = Field(default=True, description="Se o usuário está ativo")


class UsuarioCreate(UsuarioBase):
    """Schema para criação de Usuário."""
    senha: str = Field(..., min_length=8, max_length=100, description="Senha do usuário")


class UsuarioUpdate(BaseModel):
    """Schema para atualização de Usuário."""
    nome: Optional[str] = Field(None, min_length=1, max_length=255, description="Nome do usuário")
    email: Optional[EmailStr] = Field(None, description="Email do usuário")
    role: Optional[RoleEnum] = Field(None, description="Papel do usuário no sistema")
    ativo: Optional[bool] = Field(None, description="Se o usuário está ativo")
    senha: Optional[str] = Field(None, min_length=8, max_length=100, description="Nova senha do usuário")


class UsuarioResponse(UsuarioBase):
    """Schema de resposta de Usuário."""
    id: int
    criado_em: datetime
    atualizado_em: datetime

    model_config = ConfigDict(from_attributes=True)


class UsuarioInDB(UsuarioResponse):
    """Schema de Usuário com senha hash (uso interno)."""
    senha_hash: str
