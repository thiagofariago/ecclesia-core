"""
Router de Contribuições.
Endpoints CRUD para gerenciamento de contribuições.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.database import get_db
from app.schemas.contribuicao import ContribuicaoCreate, ContribuicaoUpdate, ContribuicaoResponse
from app.schemas.pagination import PaginatedResponse
from app.models.usuario import Usuario
from app.models.contribuicao import TipoContribuicaoEnum
from app.services import contribuicao_service
from app.auth.dependencies import get_current_active_user
import math

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("", response_model=PaginatedResponse[ContribuicaoResponse])
@limiter.limit("100/minute")
async def list_contribuicoes(
    request: Request,
    page: int = Query(1, ge=1, description="Número da página (1-indexed)"),
    page_size: int = Query(20, ge=1, le=100, description="Tamanho da página"),
    dizimista_id: Optional[int] = Query(None, description="Filtrar por ID do dizimista"),
    comunidade_id: Optional[int] = Query(None, description="Filtrar por ID da comunidade"),
    tipo: Optional[TipoContribuicaoEnum] = Query(None, description="Filtrar por tipo"),
    data_inicio: Optional[date] = Query(None, description="Data de início do período"),
    data_fim: Optional[date] = Query(None, description="Data de fim do período"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Lista contribuições com paginação e filtros.
    Rate limit: 100 requisições por minuto por IP.

    Args:
        request: Request object para rate limiting
        page: Número da página
        page_size: Tamanho da página
        dizimista_id: ID do dizimista para filtrar
        comunidade_id: ID da comunidade para filtrar
        tipo: Tipo de contribuição para filtrar
        data_inicio: Data de início do período
        data_fim: Data de fim do período
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Resposta paginada com contribuições
    """
    contribuicoes, total = contribuicao_service.get_contribuicoes(
        db,
        page=page,
        page_size=page_size,
        dizimista_id=dizimista_id,
        comunidade_id=comunidade_id,
        tipo=tipo,
        data_inicio=data_inicio,
        data_fim=data_fim
    )

    total_pages = math.ceil(total / page_size) if total > 0 else 0

    return {
        "items": contribuicoes,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }


@router.post("", response_model=ContribuicaoResponse, status_code=status.HTTP_201_CREATED)
async def create_contribuicao(
    contribuicao_data: ContribuicaoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Cria uma nova contribuição.

    Args:
        contribuicao_data: Dados da contribuição
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Contribuição criada
    """
    contribuicao = contribuicao_service.create_contribuicao(db, contribuicao_data)
    return contribuicao


@router.get("/{contribuicao_id}", response_model=ContribuicaoResponse)
async def get_contribuicao(
    contribuicao_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Obtém uma contribuição por ID.

    Args:
        contribuicao_id: ID da contribuição
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Contribuição encontrada

    Raises:
        HTTPException: Se a contribuição não for encontrada
    """
    contribuicao = contribuicao_service.get_contribuicao(db, contribuicao_id)
    if not contribuicao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contribuição não encontrada"
        )
    return contribuicao


@router.patch("/{contribuicao_id}", response_model=ContribuicaoResponse)
async def update_contribuicao(
    contribuicao_id: int,
    contribuicao_data: ContribuicaoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Atualiza uma contribuição.

    Args:
        contribuicao_id: ID da contribuição
        contribuicao_data: Dados para atualização
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Contribuição atualizada

    Raises:
        HTTPException: Se a contribuição não for encontrada
    """
    contribuicao = contribuicao_service.update_contribuicao(db, contribuicao_id, contribuicao_data)
    if not contribuicao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contribuição não encontrada"
        )
    return contribuicao


@router.delete("/{contribuicao_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contribuicao(
    contribuicao_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Deleta uma contribuição.

    Args:
        contribuicao_id: ID da contribuição
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Raises:
        HTTPException: Se a contribuição não for encontrada
    """
    deleted = contribuicao_service.delete_contribuicao(db, contribuicao_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contribuição não encontrada"
        )
