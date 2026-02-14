"""
Serviço de Comunidade.
Lógica de negócio para operações CRUD de comunidades.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.comunidade import Comunidade
from app.models.dizimista import Dizimista
from app.schemas.comunidade import ComunidadeCreate, ComunidadeUpdate


def get_comunidade(db: Session, comunidade_id: int) -> Optional[Comunidade]:
    """
    Obtém uma comunidade por ID.

    Args:
        db: Sessão do banco de dados
        comunidade_id: ID da comunidade

    Returns:
        Comunidade encontrada ou None
    """
    return db.query(Comunidade).filter(Comunidade.id == comunidade_id).first()


def get_comunidades(db: Session, paroquia_id: Optional[int] = None) -> List[Comunidade]:
    """
    Obtém comunidades, opcionalmente filtradas por paróquia.

    Args:
        db: Sessão do banco de dados
        paroquia_id: ID da paróquia para filtrar (opcional)

    Returns:
        Lista de comunidades
    """
    query = db.query(Comunidade)
    if paroquia_id is not None:
        query = query.filter(Comunidade.paroquia_id == paroquia_id)
    return query.order_by(Comunidade.nome).all()


def create_comunidade(db: Session, comunidade_data: ComunidadeCreate) -> Comunidade:
    """
    Cria uma nova comunidade.

    Args:
        db: Sessão do banco de dados
        comunidade_data: Dados da comunidade

    Returns:
        Comunidade criada
    """
    db_comunidade = Comunidade(**comunidade_data.model_dump())
    db.add(db_comunidade)
    db.commit()
    db.refresh(db_comunidade)
    return db_comunidade


def update_comunidade(db: Session, comunidade_id: int, comunidade_data: ComunidadeUpdate) -> Optional[Comunidade]:
    """
    Atualiza uma comunidade.

    Args:
        db: Sessão do banco de dados
        comunidade_id: ID da comunidade
        comunidade_data: Dados para atualização

    Returns:
        Comunidade atualizada ou None se não encontrada
    """
    db_comunidade = get_comunidade(db, comunidade_id)
    if not db_comunidade:
        return None

    update_data = comunidade_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_comunidade, key, value)

    db.commit()
    db.refresh(db_comunidade)
    return db_comunidade


def delete_comunidade(db: Session, comunidade_id: int) -> bool:
    """
    Deleta uma comunidade.

    Args:
        db: Sessão do banco de dados
        comunidade_id: ID da comunidade

    Returns:
        True se deletada, False se não encontrada

    Raises:
        HTTPException: Se a comunidade tiver dizimistas associados
    """
    db_comunidade = get_comunidade(db, comunidade_id)
    if not db_comunidade:
        return False

    # Verifica se há dizimistas associados
    dizimistas_count = db.query(Dizimista).filter(Dizimista.comunidade_id == comunidade_id).count()
    if dizimistas_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Não é possível deletar a comunidade pois ela possui {dizimistas_count} dizimista(s) associado(s)"
        )

    db.delete(db_comunidade)
    db.commit()
    return True
