"""
Schemas para Dizimista.
"""
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class DizimistaBase(BaseModel):
    """Schema base de Dizimista."""
    nome: str = Field(..., min_length=1, max_length=255, description="Nome do dizimista")
    comunidade_id: int = Field(..., description="ID da comunidade")
    cpf: Optional[str] = Field(None, max_length=14, description="CPF do dizimista")
    telefone: Optional[str] = Field(None, max_length=20, description="Telefone do dizimista")
    email: Optional[EmailStr] = Field(None, description="Email do dizimista")
    data_nascimento: Optional[date] = Field(None, description="Data de nascimento do dizimista")
    endereco: Optional[str] = Field(None, description="Endereço do dizimista")
    ativo: bool = Field(default=True, description="Se o dizimista está ativo")
    observacoes: Optional[str] = Field(None, description="Observações sobre o dizimista")


class DizimistaCreate(DizimistaBase):
    """Schema para criação de Dizimista."""
    pass


class DizimistaUpdate(BaseModel):
    """Schema para atualização de Dizimista."""
    nome: Optional[str] = Field(None, min_length=1, max_length=255, description="Nome do dizimista")
    comunidade_id: Optional[int] = Field(None, description="ID da comunidade")
    cpf: Optional[str] = Field(None, max_length=14, description="CPF do dizimista")
    telefone: Optional[str] = Field(None, max_length=20, description="Telefone do dizimista")
    email: Optional[EmailStr] = Field(None, description="Email do dizimista")
    data_nascimento: Optional[date] = Field(None, description="Data de nascimento do dizimista")
    endereco: Optional[str] = Field(None, description="Endereço do dizimista")
    ativo: Optional[bool] = Field(None, description="Se o dizimista está ativo")
    observacoes: Optional[str] = Field(None, description="Observações sobre o dizimista")


class DizimistaResponse(DizimistaBase):
    """Schema de resposta de Dizimista."""
    id: int
    criado_em: datetime
    atualizado_em: datetime

    model_config = ConfigDict(from_attributes=True)
