"""
Schemas para Comunidade.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ComunidadeBase(BaseModel):
    """Schema base de Comunidade."""
    nome: str = Field(..., min_length=1, max_length=255, description="Nome da comunidade")
    paroquia_id: int = Field(..., description="ID da paróquia")


class ComunidadeCreate(ComunidadeBase):
    """Schema para criação de Comunidade."""
    pass


class ComunidadeUpdate(BaseModel):
    """Schema para atualização de Comunidade."""
    nome: Optional[str] = Field(None, min_length=1, max_length=255, description="Nome da comunidade")
    paroquia_id: Optional[int] = Field(None, description="ID da paróquia")


class ComunidadeResponse(ComunidadeBase):
    """Schema de resposta de Comunidade."""
    id: int
    criado_em: datetime
    atualizado_em: datetime

    model_config = ConfigDict(from_attributes=True)
