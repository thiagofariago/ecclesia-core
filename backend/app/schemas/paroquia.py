"""
Schemas para Paróquia.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ParoquiaBase(BaseModel):
    """Schema base de Paróquia."""
    nome: str = Field(..., min_length=1, max_length=255, description="Nome da paróquia")


class ParoquiaCreate(ParoquiaBase):
    """Schema para criação de Paróquia."""
    pass


class ParoquiaUpdate(BaseModel):
    """Schema para atualização de Paróquia."""
    nome: Optional[str] = Field(None, min_length=1, max_length=255, description="Nome da paróquia")


class ParoquiaResponse(ParoquiaBase):
    """Schema de resposta de Paróquia."""
    id: int
    criado_em: datetime
    atualizado_em: datetime

    model_config = ConfigDict(from_attributes=True)
