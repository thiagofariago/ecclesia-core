"""
Schemas Pydantic.
Schemas de validação e serialização de dados da API.
"""
from app.schemas.pagination import PaginatedResponse
from app.schemas.auth import Login, Token, TokenData
from app.schemas.usuario import (
    UsuarioBase,
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse,
    UsuarioInDB,
)
from app.schemas.paroquia import (
    ParoquiaBase,
    ParoquiaCreate,
    ParoquiaUpdate,
    ParoquiaResponse,
)
from app.schemas.comunidade import (
    ComunidadeBase,
    ComunidadeCreate,
    ComunidadeUpdate,
    ComunidadeResponse,
)
from app.schemas.dizimista import (
    DizimistaBase,
    DizimistaCreate,
    DizimistaUpdate,
    DizimistaResponse,
)
from app.schemas.contribuicao import (
    ContribuicaoBase,
    ContribuicaoCreate,
    ContribuicaoUpdate,
    ContribuicaoResponse,
)
from app.schemas.reports import (
    AniversarianteResponse,
    TotalPeriodoResponse,
    TotalTipoResponse,
    TotalTipoListResponse,
    HistoricoContribuicaoResponse,
)

__all__ = [
    "PaginatedResponse",
    "Login",
    "Token",
    "TokenData",
    "UsuarioBase",
    "UsuarioCreate",
    "UsuarioUpdate",
    "UsuarioResponse",
    "UsuarioInDB",
    "ParoquiaBase",
    "ParoquiaCreate",
    "ParoquiaUpdate",
    "ParoquiaResponse",
    "ComunidadeBase",
    "ComunidadeCreate",
    "ComunidadeUpdate",
    "ComunidadeResponse",
    "DizimistaBase",
    "DizimistaCreate",
    "DizimistaUpdate",
    "DizimistaResponse",
    "ContribuicaoBase",
    "ContribuicaoCreate",
    "ContribuicaoUpdate",
    "ContribuicaoResponse",
    "AniversarianteResponse",
    "TotalPeriodoResponse",
    "TotalTipoResponse",
    "TotalTipoListResponse",
    "HistoricoContribuicaoResponse",
]
