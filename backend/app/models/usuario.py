"""
Modelo de Usuário do sistema.
Gerencia autenticação e autorização de usuários.
"""
from enum import Enum
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func

from app.database import Base


class RoleEnum(str, Enum):
    """Enum para papéis de usuários."""
    ADMIN = "ADMIN"
    OPERADOR = "OPERADOR"


class Usuario(Base):
    """Modelo de Usuário."""
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(RoleEnum), nullable=False, default=RoleEnum.OPERADOR)
    ativo = Column(Boolean, nullable=False, default=True, index=True)

    # Timestamps
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<Usuario(id={self.id}, email={self.email}, role={self.role})>"
