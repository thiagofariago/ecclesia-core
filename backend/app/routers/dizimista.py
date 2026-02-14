"""
Router de Dizimistas.
Endpoints CRUD para gerenciamento de dizimistas.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.database import get_db
from app.schemas.dizimista import DizimistaCreate, DizimistaUpdate, DizimistaResponse
from app.schemas.pagination import PaginatedResponse
from app.models.usuario import Usuario
from app.services import dizimista_service
from app.auth.dependencies import get_current_active_user
import math

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("", response_model=PaginatedResponse[DizimistaResponse])
@limiter.limit("100/minute")
async def list_dizimistas(
    request: Request,
    page: int = Query(1, ge=1, description="Número da página (1-indexed)"),
    page_size: int = Query(20, ge=1, le=100, description="Tamanho da página"),
    search: Optional[str] = Query(None, description="Buscar por nome, telefone ou email"),
    comunidade_id: Optional[int] = Query(None, description="Filtrar por ID da comunidade"),
    ativo: Optional[bool] = Query(None, description="Filtrar por status ativo"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Lista dizimistas com paginação e filtros.
    Rate limit: 100 requisições por minuto por IP.

    Args:
        request: Request object para rate limiting
        page: Número da página
        page_size: Tamanho da página
        search: Termo de busca
        comunidade_id: ID da comunidade para filtrar
        ativo: Status ativo para filtrar
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Resposta paginada com dizimistas
    """
    dizimistas, total = dizimista_service.get_dizimistas(
        db,
        page=page,
        page_size=page_size,
        search=search,
        comunidade_id=comunidade_id,
        ativo=ativo
    )

    total_pages = math.ceil(total / page_size) if total > 0 else 0

    return {
        "items": dizimistas,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }


@router.post("", response_model=DizimistaResponse, status_code=status.HTTP_201_CREATED)
async def create_dizimista(
    dizimista_data: DizimistaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Cria um novo dizimista.

    Args:
        dizimista_data: Dados do dizimista
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Dizimista criado

    Raises:
        HTTPException: Se o CPF já estiver cadastrado
    """
    try:
        dizimista = dizimista_service.create_dizimista(db, dizimista_data)
        return dizimista
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF já cadastrado no sistema"
        )


@router.get("/{dizimista_id}", response_model=DizimistaResponse)
async def get_dizimista(
    dizimista_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Obtém um dizimista por ID.

    Args:
        dizimista_id: ID do dizimista
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Dizimista encontrado

    Raises:
        HTTPException: Se o dizimista não for encontrado
    """
    dizimista = dizimista_service.get_dizimista(db, dizimista_id)
    if not dizimista:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dizimista não encontrado"
        )
    return dizimista


@router.patch("/{dizimista_id}", response_model=DizimistaResponse)
async def update_dizimista(
    dizimista_id: int,
    dizimista_data: DizimistaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Atualiza um dizimista.

    Args:
        dizimista_id: ID do dizimista
        dizimista_data: Dados para atualização
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Dizimista atualizado

    Raises:
        HTTPException: Se o dizimista não for encontrado ou CPF duplicado
    """
    try:
        dizimista = dizimista_service.update_dizimista(db, dizimista_id, dizimista_data)
        if not dizimista:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dizimista não encontrado"
            )
        return dizimista
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF já cadastrado no sistema"
        )


@router.delete("/{dizimista_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dizimista(
    dizimista_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Soft delete de um dizimista (marca como inativo).

    Args:
        dizimista_id: ID do dizimista
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Raises:
        HTTPException: Se o dizimista não for encontrado
    """
    deleted = dizimista_service.delete_dizimista(db, dizimista_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dizimista não encontrado"
        )
