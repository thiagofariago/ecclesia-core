"""
Models package.
Importa todos os modelos SQLAlchemy para que o Alembic possa detectá-los.
"""
from app.database import Base
from app.models.usuario import Usuario, RoleEnum
from app.models.paroquia import Paroquia
from app.models.comunidade import Comunidade
from app.models.dizimista import Dizimista
from app.models.contribuicao import Contribuicao, TipoContribuicaoEnum

__all__ = [
    "Base",
    "Usuario",
    "RoleEnum",
    "Paroquia",
    "Comunidade",
    "Dizimista",
    "Contribuicao",
    "TipoContribuicaoEnum",
]
