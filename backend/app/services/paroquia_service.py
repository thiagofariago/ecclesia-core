"""
Serviço de Paróquia.
Lógica de negócio para operações CRUD de paróquias.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.paroquia import Paroquia
from app.models.comunidade import Comunidade
from app.schemas.paroquia import ParoquiaCreate, ParoquiaUpdate


def get_paroquia(db: Session, paroquia_id: int) -> Optional[Paroquia]:
    """
    Obtém uma paróquia por ID.

    Args:
        db: Sessão do banco de dados
        paroquia_id: ID da paróquia

    Returns:
        Paróquia encontrada ou None
    """
    return db.query(Paroquia).filter(Paroquia.id == paroquia_id).first()


def get_paroquias(db: Session) -> List[Paroquia]:
    """
    Obtém todas as paróquias.

    Args:
        db: Sessão do banco de dados

    Returns:
        Lista de paróquias
    """
    return db.query(Paroquia).order_by(Paroquia.nome).all()


def create_paroquia(db: Session, paroquia_data: ParoquiaCreate) -> Paroquia:
    """
    Cria uma nova paróquia.

    Args:
        db: Sessão do banco de dados
        paroquia_data: Dados da paróquia

    Returns:
        Paróquia criada
    """
    db_paroquia = Paroquia(**paroquia_data.model_dump())
    db.add(db_paroquia)
    db.commit()
    db.refresh(db_paroquia)
    return db_paroquia


def update_paroquia(db: Session, paroquia_id: int, paroquia_data: ParoquiaUpdate) -> Optional[Paroquia]:
    """
    Atualiza uma paróquia.

    Args:
        db: Sessão do banco de dados
        paroquia_id: ID da paróquia
        paroquia_data: Dados para atualização

    Returns:
        Paróquia atualizada ou None se não encontrada
    """
    db_paroquia = get_paroquia(db, paroquia_id)
    if not db_paroquia:
        return None

    update_data = paroquia_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_paroquia, key, value)

    db.commit()
    db.refresh(db_paroquia)
    return db_paroquia


def delete_paroquia(db: Session, paroquia_id: int) -> bool:
    """
    Deleta uma paróquia.

    Args:
        db: Sessão do banco de dados
        paroquia_id: ID da paróquia

    Returns:
        True se deletada, False se não encontrada

    Raises:
        HTTPException: Se a paróquia tiver comunidades associadas
    """
    db_paroquia = get_paroquia(db, paroquia_id)
    if not db_paroquia:
        return False

    # Verifica se há comunidades associadas
    comunidades_count = db.query(Comunidade).filter(Comunidade.paroquia_id == paroquia_id).count()
    if comunidades_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Não é possível deletar a paróquia pois ela possui {comunidades_count} comunidade(s) associada(s)"
        )

    db.delete(db_paroquia)
    db.commit()
    return True
