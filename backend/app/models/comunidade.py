"""
Modelo de Comunidade.
Representa uma comunidade pertencente a uma paróquia.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Comunidade(Base):
    """Modelo de Comunidade."""
    __tablename__ = "comunidades"

    id = Column(Integer, primary_key=True, index=True)
    paroquia_id = Column(Integer, ForeignKey("paroquias.id", ondelete="RESTRICT"), nullable=False, index=True)
    nome = Column(String(255), nullable=False, index=True)

    # Timestamps
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relacionamentos
    paroquia = relationship("Paroquia", back_populates="comunidades")
    dizimistas = relationship("Dizimista", back_populates="comunidade", cascade="all, delete-orphan")
    contribuicoes = relationship("Contribuicao", back_populates="comunidade")

    def __repr__(self):
        return f"<Comunidade(id={self.id}, nome={self.nome}, paroquia_id={self.paroquia_id})>"
