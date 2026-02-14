"""
Schemas para relatórios.
"""
from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

from app.models.contribuicao import TipoContribuicaoEnum


class AniversarianteResponse(BaseModel):
    """Schema de resposta para aniversariantes."""
    id: int
    nome: str
    data_nascimento: date
    telefone: Optional[str] = None
    email: Optional[str] = None
    comunidade_id: int
    comunidade_nome: str

    model_config = ConfigDict(from_attributes=True)


class TotalPeriodoResponse(BaseModel):
    """Schema de resposta para total por período."""
    total: Decimal = Field(..., description="Total de contribuições no período")
    quantidade: int = Field(..., description="Quantidade de contribuições")
    data_inicio: date = Field(..., description="Data de início do período")
    data_fim: date = Field(..., description="Data de fim do período")
    comunidade_id: Optional[int] = Field(None, description="ID da comunidade filtrada (se aplicável)")


class TotalTipoResponse(BaseModel):
    """Schema de resposta para total por tipo."""
    tipo: TipoContribuicaoEnum = Field(..., description="Tipo da contribuição")
    total: Decimal = Field(..., description="Total do tipo")
    quantidade: int = Field(..., description="Quantidade de contribuições do tipo")


class TotalTipoListResponse(BaseModel):
    """Schema de resposta para lista de totais por tipo."""
    data_inicio: date = Field(..., description="Data de início do período")
    data_fim: date = Field(..., description="Data de fim do período")
    comunidade_id: Optional[int] = Field(None, description="ID da comunidade filtrada (se aplicável)")
    totais: list[TotalTipoResponse] = Field(..., description="Lista de totais por tipo")


class HistoricoContribuicaoResponse(BaseModel):
    """Schema de resposta para histórico de contribuições de um dizimista."""
    dizimista_id: int
    dizimista_nome: str
    total_geral: Decimal
    quantidade_total: int
    contribuicoes: list = Field(..., description="Lista de contribuições do dizimista")

    model_config = ConfigDict(from_attributes=True)
