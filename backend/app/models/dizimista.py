"""
Modelo de Dizimista.
Representa um dizimista (membro contribuinte) de uma comunidade.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Date, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Dizimista(Base):
    """Modelo de Dizimista."""
    __tablename__ = "dizimistas"

    id = Column(Integer, primary_key=True, index=True)
    comunidade_id = Column(Integer, ForeignKey("comunidades.id", ondelete="RESTRICT"), nullable=False, index=True)
    nome = Column(String(255), nullable=False, index=True)
    cpf = Column(String(14), nullable=True, unique=True, index=True)  # Format: 000.000.000-00
    telefone = Column(String(20), nullable=True, index=True)
    email = Column(String(255), nullable=True, index=True)
    data_nascimento = Column(Date, nullable=True, index=True)
    endereco = Column(Text, nullable=True)
    ativo = Column(Boolean, nullable=False, default=True, index=True)
    observacoes = Column(Text, nullable=True)

    # Timestamps
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relacionamentos
    comunidade = relationship("Comunidade", back_populates="dizimistas")
    contribuicoes = relationship("Contribuicao", back_populates="dizimista")

    def __repr__(self):
        return f"<Dizimista(id={self.id}, nome={self.nome}, ativo={self.ativo})>"
