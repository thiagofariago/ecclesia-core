"""
Schemas para Contribuição.
"""
from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator

from app.models.contribuicao import TipoContribuicaoEnum


class ContribuicaoBase(BaseModel):
    """Schema base de Contribuição."""
    dizimista_id: Optional[int] = Field(None, description="ID do dizimista (opcional)")
    comunidade_id: int = Field(..., description="ID da comunidade")
    tipo: TipoContribuicaoEnum = Field(..., description="Tipo da contribuição")
    valor: Decimal = Field(..., gt=0, description="Valor da contribuição (deve ser maior que zero)")
    data_contribuicao: date = Field(..., description="Data da contribuição")
    forma_pagamento: Optional[str] = Field(None, max_length=100, description="Forma de pagamento")
    referencia_mes: Optional[str] = Field(None, max_length=7, description="Mês de referência (YYYY-MM)")
    observacoes: Optional[str] = Field(None, description="Observações sobre a contribuição")

    @field_validator("referencia_mes")
    @classmethod
    def validate_referencia_mes(cls, v: Optional[str]) -> Optional[str]:
        """Valida formato YYYY-MM."""
        if v is not None:
            parts = v.split("-")
            if len(parts) != 2 or len(parts[0]) != 4 or len(parts[1]) != 2:
                raise ValueError("referencia_mes deve estar no formato YYYY-MM")
            try:
                year = int(parts[0])
                month = int(parts[1])
                if month < 1 or month > 12:
                    raise ValueError("Mês deve estar entre 01 e 12")
            except ValueError:
                raise ValueError("referencia_mes deve conter ano e mês válidos")
        return v


class ContribuicaoCreate(ContribuicaoBase):
    """Schema para criação de Contribuição."""
    pass


class ContribuicaoUpdate(BaseModel):
    """Schema para atualização de Contribuição."""
    dizimista_id: Optional[int] = Field(None, description="ID do dizimista (opcional)")
    comunidade_id: Optional[int] = Field(None, description="ID da comunidade")
    tipo: Optional[TipoContribuicaoEnum] = Field(None, description="Tipo da contribuição")
    valor: Optional[Decimal] = Field(None, gt=0, description="Valor da contribuição (deve ser maior que zero)")
    data_contribuicao: Optional[date] = Field(None, description="Data da contribuição")
    forma_pagamento: Optional[str] = Field(None, max_length=100, description="Forma de pagamento")
    referencia_mes: Optional[str] = Field(None, max_length=7, description="Mês de referência (YYYY-MM)")
    observacoes: Optional[str] = Field(None, description="Observações sobre a contribuição")

    @field_validator("referencia_mes")
    @classmethod
    def validate_referencia_mes(cls, v: Optional[str]) -> Optional[str]:
        """Valida formato YYYY-MM."""
        if v is not None:
            parts = v.split("-")
            if len(parts) != 2 or len(parts[0]) != 4 or len(parts[1]) != 2:
                raise ValueError("referencia_mes deve estar no formato YYYY-MM")
            try:
                year = int(parts[0])
                month = int(parts[1])
                if month < 1 or month > 12:
                    raise ValueError("Mês deve estar entre 01 e 12")
            except ValueError:
                raise ValueError("referencia_mes deve conter ano e mês válidos")
        return v


class ContribuicaoResponse(ContribuicaoBase):
    """Schema de resposta de Contribuição."""
    id: int
    criado_em: datetime
    atualizado_em: datetime

    model_config = ConfigDict(from_attributes=True)
