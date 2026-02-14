"""
Serviço de Dizimista.
Lógica de negócio para operações CRUD de dizimistas.
"""
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.dizimista import Dizimista
from app.schemas.dizimista import DizimistaCreate, DizimistaUpdate


def get_dizimista(db: Session, dizimista_id: int) -> Optional[Dizimista]:
    """
    Obtém um dizimista por ID.

    Args:
        db: Sessão do banco de dados
        dizimista_id: ID do dizimista

    Returns:
        Dizimista encontrado ou None
    """
    return db.query(Dizimista).filter(Dizimista.id == dizimista_id).first()


def get_dizimistas(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    search: Optional[str] = None,
    comunidade_id: Optional[int] = None,
    ativo: Optional[bool] = None,
) -> Tuple[List[Dizimista], int]:
    """
    Obtém dizimistas com paginação e filtros.

    Args:
        db: Sessão do banco de dados
        page: Página atual (1-indexed)
        page_size: Tamanho da página
        search: Termo de busca (nome, telefone, email)
        comunidade_id: ID da comunidade para filtrar
        ativo: Status ativo para filtrar

    Returns:
        Tupla com (lista de dizimistas, total de registros)
    """
    query = db.query(Dizimista)

    # Aplicar filtros
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Dizimista.nome.ilike(search_term),
                Dizimista.telefone.ilike(search_term),
                Dizimista.email.ilike(search_term),
            )
        )

    if comunidade_id is not None:
        query = query.filter(Dizimista.comunidade_id == comunidade_id)

    if ativo is not None:
        query = query.filter(Dizimista.ativo == ativo)

    # Contar total
    total = query.count()

    # Aplicar paginação
    offset = (page - 1) * page_size
    dizimistas = query.order_by(Dizimista.nome).offset(offset).limit(page_size).all()

    return dizimistas, total


def create_dizimista(db: Session, dizimista_data: DizimistaCreate) -> Dizimista:
    """
    Cria um novo dizimista.

    Args:
        db: Sessão do banco de dados
        dizimista_data: Dados do dizimista

    Returns:
        Dizimista criado
    """
    db_dizimista = Dizimista(**dizimista_data.model_dump())
    db.add(db_dizimista)
    db.commit()
    db.refresh(db_dizimista)
    return db_dizimista


def update_dizimista(db: Session, dizimista_id: int, dizimista_data: DizimistaUpdate) -> Optional[Dizimista]:
    """
    Atualiza um dizimista.

    Args:
        db: Sessão do banco de dados
        dizimista_id: ID do dizimista
        dizimista_data: Dados para atualização

    Returns:
        Dizimista atualizado ou None se não encontrado
    """
    db_dizimista = get_dizimista(db, dizimista_id)
    if not db_dizimista:
        return None

    update_data = dizimista_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_dizimista, key, value)

    db.commit()
    db.refresh(db_dizimista)
    return db_dizimista


def delete_dizimista(db: Session, dizimista_id: int) -> bool:
    """
    Soft delete de um dizimista (marca como inativo).

    Args:
        db: Sessão do banco de dados
        dizimista_id: ID do dizimista

    Returns:
        True se marcado como inativo, False se não encontrado
    """
    db_dizimista = get_dizimista(db, dizimista_id)
    if not db_dizimista:
        return False

    db_dizimista.ativo = False
    db.commit()
    return True
