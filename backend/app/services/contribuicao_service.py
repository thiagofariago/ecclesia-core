"""
Serviço de Contribuição.
Lógica de negócio para operações CRUD de contribuições.
"""
from datetime import date
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session

from app.models.contribuicao import Contribuicao, TipoContribuicaoEnum
from app.schemas.contribuicao import ContribuicaoCreate, ContribuicaoUpdate


def get_contribuicao(db: Session, contribuicao_id: int) -> Optional[Contribuicao]:
    """
    Obtém uma contribuição por ID.

    Args:
        db: Sessão do banco de dados
        contribuicao_id: ID da contribuição

    Returns:
        Contribuição encontrada ou None
    """
    return db.query(Contribuicao).filter(Contribuicao.id == contribuicao_id).first()


def get_contribuicoes(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    dizimista_id: Optional[int] = None,
    comunidade_id: Optional[int] = None,
    tipo: Optional[TipoContribuicaoEnum] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
) -> Tuple[List[Contribuicao], int]:
    """
    Obtém contribuições com paginação e filtros.

    Args:
        db: Sessão do banco de dados
        page: Página atual (1-indexed)
        page_size: Tamanho da página
        dizimista_id: ID do dizimista para filtrar
        comunidade_id: ID da comunidade para filtrar
        tipo: Tipo de contribuição para filtrar
        data_inicio: Data de início do período
        data_fim: Data de fim do período

    Returns:
        Tupla com (lista de contribuições, total de registros)
    """
    query = db.query(Contribuicao)

    # Aplicar filtros
    if dizimista_id is not None:
        query = query.filter(Contribuicao.dizimista_id == dizimista_id)

    if comunidade_id is not None:
        query = query.filter(Contribuicao.comunidade_id == comunidade_id)

    if tipo is not None:
        query = query.filter(Contribuicao.tipo == tipo)

    if data_inicio is not None:
        query = query.filter(Contribuicao.data_contribuicao >= data_inicio)

    if data_fim is not None:
        query = query.filter(Contribuicao.data_contribuicao <= data_fim)

    # Contar total
    total = query.count()

    # Aplicar paginação
    offset = (page - 1) * page_size
    contribuicoes = (
        query.order_by(Contribuicao.data_contribuicao.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return contribuicoes, total


def create_contribuicao(db: Session, contribuicao_data: ContribuicaoCreate) -> Contribuicao:
    """
    Cria uma nova contribuição.

    Args:
        db: Sessão do banco de dados
        contribuicao_data: Dados da contribuição

    Returns:
        Contribuição criada
    """
    db_contribuicao = Contribuicao(**contribuicao_data.model_dump())
    db.add(db_contribuicao)
    db.commit()
    db.refresh(db_contribuicao)
    return db_contribuicao


def update_contribuicao(
    db: Session,
    contribuicao_id: int,
    contribuicao_data: ContribuicaoUpdate
) -> Optional[Contribuicao]:
    """
    Atualiza uma contribuição.

    Args:
        db: Sessão do banco de dados
        contribuicao_id: ID da contribuição
        contribuicao_data: Dados para atualização

    Returns:
        Contribuição atualizada ou None se não encontrada
    """
    db_contribuicao = get_contribuicao(db, contribuicao_id)
    if not db_contribuicao:
        return None

    update_data = contribuicao_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_contribuicao, key, value)

    db.commit()
    db.refresh(db_contribuicao)
    return db_contribuicao


def delete_contribuicao(db: Session, contribuicao_id: int) -> bool:
    """
    Deleta uma contribuição (hard delete).

    Args:
        db: Sessão do banco de dados
        contribuicao_id: ID da contribuição

    Returns:
        True se deletada, False se não encontrada
    """
    db_contribuicao = get_contribuicao(db, contribuicao_id)
    if not db_contribuicao:
        return False

    db.delete(db_contribuicao)
    db.commit()
    return True
