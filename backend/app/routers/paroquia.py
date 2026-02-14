"""
Router de Paróquias.
Endpoints CRUD para gerenciamento de paróquias.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.paroquia import ParoquiaCreate, ParoquiaUpdate, ParoquiaResponse
from app.models.usuario import Usuario
from app.services import paroquia_service
from app.auth.dependencies import get_current_active_user, require_admin

router = APIRouter()


@router.get("", response_model=List[ParoquiaResponse])
async def list_paroquias(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Lista todas as paróquias.

    Args:
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Lista de paróquias
    """
    paroquias = paroquia_service.get_paroquias(db)
    return paroquias


@router.post("", response_model=ParoquiaResponse, status_code=status.HTTP_201_CREATED)
async def create_paroquia(
    paroquia_data: ParoquiaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """
    Cria uma nova paróquia (apenas administradores).

    Args:
        paroquia_data: Dados da paróquia
        db: Sessão do banco de dados
        current_user: Usuário autenticado (deve ser admin)

    Returns:
        Paróquia criada
    """
    paroquia = paroquia_service.create_paroquia(db, paroquia_data)
    return paroquia


@router.get("/{paroquia_id}", response_model=ParoquiaResponse)
async def get_paroquia(
    paroquia_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Obtém uma paróquia por ID.

    Args:
        paroquia_id: ID da paróquia
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Paróquia encontrada

    Raises:
        HTTPException: Se a paróquia não for encontrada
    """
    paroquia = paroquia_service.get_paroquia(db, paroquia_id)
    if not paroquia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paróquia não encontrada"
        )
    return paroquia


@router.patch("/{paroquia_id}", response_model=ParoquiaResponse)
async def update_paroquia(
    paroquia_id: int,
    paroquia_data: ParoquiaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """
    Atualiza uma paróquia (apenas administradores).

    Args:
        paroquia_id: ID da paróquia
        paroquia_data: Dados para atualização
        db: Sessão do banco de dados
        current_user: Usuário autenticado (deve ser admin)

    Returns:
        Paróquia atualizada

    Raises:
        HTTPException: Se a paróquia não for encontrada
    """
    paroquia = paroquia_service.update_paroquia(db, paroquia_id, paroquia_data)
    if not paroquia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paróquia não encontrada"
        )
    return paroquia


@router.delete("/{paroquia_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_paroquia(
    paroquia_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """
    Deleta uma paróquia (apenas administradores).

    Args:
        paroquia_id: ID da paróquia
        db: Sessão do banco de dados
        current_user: Usuário autenticado (deve ser admin)

    Raises:
        HTTPException: Se a paróquia não for encontrada ou tiver comunidades associadas
    """
    deleted = paroquia_service.delete_paroquia(db, paroquia_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paróquia não encontrada"
        )
