"""
Modelo de Contribuição.
Representa uma contribuição (dízimo ou oferta) de um dizimista ou comunidade.
"""
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Numeric, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class TipoContribuicaoEnum(str, Enum):
    """Enum para tipos de contribuição."""
    DIZIMO = "DIZIMO"
    OFERTA = "OFERTA"


class Contribuicao(Base):
    """Modelo de Contribuição."""
    __tablename__ = "contribuicoes"

    id = Column(Integer, primary_key=True, index=True)
    dizimista_id = Column(Integer, ForeignKey("dizimistas.id", ondelete="SET NULL"), nullable=True, index=True)
    comunidade_id = Column(Integer, ForeignKey("comunidades.id", ondelete="RESTRICT"), nullable=False, index=True)
    tipo = Column(SQLEnum(TipoContribuicaoEnum), nullable=False, index=True)
    valor = Column(Numeric(precision=10, scale=2), nullable=False)
    data_contribuicao = Column(Date, nullable=False, index=True)
    forma_pagamento = Column(String(100), nullable=True)  # Ex: Dinheiro, PIX, Cartão, etc.
    referencia_mes = Column(String(7), nullable=True, index=True)  # Format: YYYY-MM
    observacoes = Column(Text, nullable=True)

    # Timestamps
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relacionamentos
    dizimista = relationship("Dizimista", back_populates="contribuicoes")
    comunidade = relationship("Comunidade", back_populates="contribuicoes")

    def __repr__(self):
        return f"<Contribuicao(id={self.id}, tipo={self.tipo}, valor={self.valor}, data={self.data_contribuicao})>"
