"""
Router de Relatórios.
Endpoints para geração de relatórios e estatísticas.
"""
from datetime import date
from typing import Optional, Literal, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.reports import (
    AniversarianteResponse,
    TotalPeriodoResponse,
    TotalTipoListResponse,
    HistoricoContribuicaoResponse,
)
from app.models.usuario import Usuario
from app.services import report_service
from app.auth.dependencies import get_current_active_user

router = APIRouter()


@router.get("/aniversariantes", response_model=List[AniversarianteResponse])
async def get_aniversariantes(
    periodo: Literal["hoje", "7dias", "mes"] = Query(..., description="Período de aniversário"),
    comunidade_id: Optional[int] = Query(None, description="Filtrar por ID da comunidade"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Obtém lista de aniversariantes.

    Args:
        periodo: Período de aniversário ('hoje', '7dias', 'mes')
        comunidade_id: ID da comunidade para filtrar (opcional)
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Lista de aniversariantes
    """
    aniversariantes = report_service.get_aniversariantes(db, periodo, comunidade_id)
    return aniversariantes


@router.get("/total-periodo", response_model=TotalPeriodoResponse)
async def get_total_periodo(
    start_date: date = Query(..., description="Data de início do período"),
    end_date: date = Query(..., description="Data de fim do período"),
    comunidade_id: Optional[int] = Query(None, description="Filtrar por ID da comunidade"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Obtém total de contribuições em um período.

    Args:
        start_date: Data de início
        end_date: Data de fim
        comunidade_id: ID da comunidade para filtrar (opcional)
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Total e quantidade de contribuições

    Raises:
        HTTPException: Se as datas forem inválidas
    """
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data de início deve ser anterior à data de fim"
        )

    result = report_service.get_total_by_period(db, start_date, end_date, comunidade_id)
    return result


@router.get("/total-tipo", response_model=TotalTipoListResponse)
async def get_total_tipo(
    start_date: date = Query(..., description="Data de início do período"),
    end_date: date = Query(..., description="Data de fim do período"),
    comunidade_id: Optional[int] = Query(None, description="Filtrar por ID da comunidade"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Obtém totais de contribuições por tipo em um período.

    Args:
        start_date: Data de início
        end_date: Data de fim
        comunidade_id: ID da comunidade para filtrar (opcional)
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Totais por tipo de contribuição

    Raises:
        HTTPException: Se as datas forem inválidas
    """
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data de início deve ser anterior à data de fim"
        )

    result = report_service.get_total_by_tipo(db, start_date, end_date, comunidade_id)
    return result


@router.get("/dizimista/{dizimista_id}/historico", response_model=HistoricoContribuicaoResponse)
async def get_dizimista_historico(
    dizimista_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Obtém histórico de contribuições de um dizimista.

    Args:
        dizimista_id: ID do dizimista
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Histórico de contribuições

    Raises:
        HTTPException: Se o dizimista não for encontrado
    """
    result = report_service.get_dizimista_history(db, dizimista_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dizimista não encontrado"
        )
    return result
