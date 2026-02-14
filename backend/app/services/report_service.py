"""
Serviço de Relatórios.
Lógica de negócio para geração de relatórios e estatísticas.
"""
from datetime import date, timedelta
from decimal import Decimal
from typing import List, Optional, Literal
from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.models.dizimista import Dizimista
from app.models.contribuicao import Contribuicao, TipoContribuicaoEnum
from app.models.comunidade import Comunidade


def get_aniversariantes(
    db: Session,
    periodo: Literal["hoje", "7dias", "mes"],
    comunidade_id: Optional[int] = None
) -> List[dict]:
    """
    Obtém dizimistas aniversariantes.

    Args:
        db: Sessão do banco de dados
        periodo: Período de aniversário ('hoje', '7dias', 'mes')
        comunidade_id: ID da comunidade para filtrar (opcional)

    Returns:
        Lista de aniversariantes
    """
    hoje = date.today()
    query = db.query(
        Dizimista.id,
        Dizimista.nome,
        Dizimista.data_nascimento,
        Dizimista.telefone,
        Dizimista.email,
        Dizimista.comunidade_id,
        Comunidade.nome.label("comunidade_nome")
    ).join(Comunidade)

    # Filtrar apenas ativos com data de nascimento
    query = query.filter(
        Dizimista.ativo == True,
        Dizimista.data_nascimento.isnot(None)
    )

    # Filtrar por comunidade se especificado
    if comunidade_id is not None:
        query = query.filter(Dizimista.comunidade_id == comunidade_id)

    # Determinar intervalo de datas baseado no período
    if periodo == "hoje":
        query = query.filter(
            extract('month', Dizimista.data_nascimento) == hoje.month,
            extract('day', Dizimista.data_nascimento) == hoje.day
        )
    elif periodo == "7dias":
        # Próximos 7 dias
        fim = hoje + timedelta(days=7)
        # Lidar com mudança de ano
        if hoje.year == fim.year:
            query = query.filter(
                extract('month', Dizimista.data_nascimento) * 100 + extract('day', Dizimista.data_nascimento) >= hoje.month * 100 + hoje.day,
                extract('month', Dizimista.data_nascimento) * 100 + extract('day', Dizimista.data_nascimento) <= fim.month * 100 + fim.day
            )
        else:
            # Aniversários até o fim do ano ou do início do ano até a data fim
            query = query.filter(
                (extract('month', Dizimista.data_nascimento) * 100 + extract('day', Dizimista.data_nascimento) >= hoje.month * 100 + hoje.day) |
                (extract('month', Dizimista.data_nascimento) * 100 + extract('day', Dizimista.data_nascimento) <= fim.month * 100 + fim.day)
            )
    elif periodo == "mes":
        query = query.filter(
            extract('month', Dizimista.data_nascimento) == hoje.month
        )

    results = query.order_by(
        extract('month', Dizimista.data_nascimento),
        extract('day', Dizimista.data_nascimento)
    ).all()

    return [
        {
            "id": r.id,
            "nome": r.nome,
            "data_nascimento": r.data_nascimento,
            "telefone": r.telefone,
            "email": r.email,
            "comunidade_id": r.comunidade_id,
            "comunidade_nome": r.comunidade_nome,
        }
        for r in results
    ]


def get_total_by_period(
    db: Session,
    start_date: date,
    end_date: date,
    comunidade_id: Optional[int] = None
) -> dict:
    """
    Obtém total de contribuições em um período.

    Args:
        db: Sessão do banco de dados
        start_date: Data de início
        end_date: Data de fim
        comunidade_id: ID da comunidade para filtrar (opcional)

    Returns:
        Dicionário com total e quantidade
    """
    query = db.query(
        func.sum(Contribuicao.valor).label("total"),
        func.count(Contribuicao.id).label("quantidade")
    ).filter(
        Contribuicao.data_contribuicao >= start_date,
        Contribuicao.data_contribuicao <= end_date
    )

    if comunidade_id is not None:
        query = query.filter(Contribuicao.comunidade_id == comunidade_id)

    result = query.first()

    return {
        "total": result.total or Decimal("0.00"),
        "quantidade": result.quantidade or 0,
        "data_inicio": start_date,
        "data_fim": end_date,
        "comunidade_id": comunidade_id,
    }


def get_total_by_tipo(
    db: Session,
    start_date: date,
    end_date: date,
    comunidade_id: Optional[int] = None
) -> dict:
    """
    Obtém totais de contribuições por tipo em um período.

    Args:
        db: Sessão do banco de dados
        start_date: Data de início
        end_date: Data de fim
        comunidade_id: ID da comunidade para filtrar (opcional)

    Returns:
        Dicionário com totais por tipo
    """
    query = db.query(
        Contribuicao.tipo,
        func.sum(Contribuicao.valor).label("total"),
        func.count(Contribuicao.id).label("quantidade")
    ).filter(
        Contribuicao.data_contribuicao >= start_date,
        Contribuicao.data_contribuicao <= end_date
    )

    if comunidade_id is not None:
        query = query.filter(Contribuicao.comunidade_id == comunidade_id)

    results = query.group_by(Contribuicao.tipo).all()

    # Garantir que todos os tipos estejam presentes
    totais = {tipo: {"tipo": tipo, "total": Decimal("0.00"), "quantidade": 0} for tipo in TipoContribuicaoEnum}

    for result in results:
        totais[result.tipo] = {
            "tipo": result.tipo,
            "total": result.total or Decimal("0.00"),
            "quantidade": result.quantidade or 0,
        }

    return {
        "data_inicio": start_date,
        "data_fim": end_date,
        "comunidade_id": comunidade_id,
        "totais": list(totais.values()),
    }


def get_dizimista_history(db: Session, dizimista_id: int) -> dict:
    """
    Obtém histórico de contribuições de um dizimista.

    Args:
        db: Sessão do banco de dados
        dizimista_id: ID do dizimista

    Returns:
        Dicionário com histórico e totais
    """
    dizimista = db.query(Dizimista).filter(Dizimista.id == dizimista_id).first()
    if not dizimista:
        return None

    # Obter contribuições
    contribuicoes = (
        db.query(Contribuicao)
        .filter(Contribuicao.dizimista_id == dizimista_id)
        .order_by(Contribuicao.data_contribuicao.desc())
        .all()
    )

    # Calcular totais
    total_geral = sum(c.valor for c in contribuicoes)
    quantidade_total = len(contribuicoes)

    return {
        "dizimista_id": dizimista.id,
        "dizimista_nome": dizimista.nome,
        "total_geral": total_geral,
        "quantidade_total": quantidade_total,
        "contribuicoes": contribuicoes,
    }
