"""
Router de Comunidades.
Endpoints CRUD para gerenciamento de comunidades.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.comunidade import ComunidadeCreate, ComunidadeUpdate, ComunidadeResponse
from app.models.usuario import Usuario
from app.services import comunidade_service
from app.auth.dependencies import get_current_active_user, require_admin

router = APIRouter()


@router.get("", response_model=List[ComunidadeResponse])
async def list_comunidades(
    paroquia_id: Optional[int] = Query(None, description="Filtrar por ID da paróquia"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Lista comunidades, opcionalmente filtradas por paróquia.

    Args:
        paroquia_id: ID da paróquia para filtrar (opcional)
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Lista de comunidades
    """
    comunidades = comunidade_service.get_comunidades(db, paroquia_id)
    return comunidades


@router.post("", response_model=ComunidadeResponse, status_code=status.HTTP_201_CREATED)
async def create_comunidade(
    comunidade_data: ComunidadeCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Cria uma nova comunidade.

    Args:
        comunidade_data: Dados da comunidade
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Comunidade criada
    """
    comunidade = comunidade_service.create_comunidade(db, comunidade_data)
    return comunidade


@router.get("/{comunidade_id}", response_model=ComunidadeResponse)
async def get_comunidade(
    comunidade_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Obtém uma comunidade por ID.

    Args:
        comunidade_id: ID da comunidade
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Comunidade encontrada

    Raises:
        HTTPException: Se a comunidade não for encontrada
    """
    comunidade = comunidade_service.get_comunidade(db, comunidade_id)
    if not comunidade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comunidade não encontrada"
        )
    return comunidade


@router.patch("/{comunidade_id}", response_model=ComunidadeResponse)
async def update_comunidade(
    comunidade_id: int,
    comunidade_data: ComunidadeUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Atualiza uma comunidade.

    Args:
        comunidade_id: ID da comunidade
        comunidade_data: Dados para atualização
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Comunidade atualizada

    Raises:
        HTTPException: Se a comunidade não for encontrada
    """
    comunidade = comunidade_service.update_comunidade(db, comunidade_id, comunidade_data)
    if not comunidade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comunidade não encontrada"
        )
    return comunidade


@router.delete("/{comunidade_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comunidade(
    comunidade_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """
    Deleta uma comunidade (apenas administradores).

    Args:
        comunidade_id: ID da comunidade
        db: Sessão do banco de dados
        current_user: Usuário autenticado (deve ser admin)

    Raises:
        HTTPException: Se a comunidade não for encontrada ou tiver dizimistas associados
    """
    deleted = comunidade_service.delete_comunidade(db, comunidade_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comunidade não encontrada"
        )
