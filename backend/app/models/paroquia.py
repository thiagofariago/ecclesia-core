"""
Modelo de Paróquia.
Representa uma paróquia que contém múltiplas comunidades.
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Paroquia(Base):
    """Modelo de Paróquia."""
    __tablename__ = "paroquias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False, index=True)

    # Timestamps
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relacionamentos
    comunidades = relationship("Comunidade", back_populates="paroquia", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Paroquia(id={self.id}, nome={self.nome})>"
