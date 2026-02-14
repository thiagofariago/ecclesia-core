"""
Testes para relatórios e estatísticas.
"""
import pytest
from fastapi import status
from datetime import date, timedelta
from decimal import Decimal


def test_get_aniversariantes_hoje(client, auth_headers, db_session, sample_comunidade):
    """Testa relatório de aniversariantes do dia."""
    from app.models.dizimista import Dizimista

    hoje = date.today()
    dizimista = Dizimista(
        nome="Aniversariante Hoje",
        comunidade_id=sample_comunidade.id,
        data_nascimento=date(1990, hoje.month, hoje.day),
        ativo=True
    )
    db_session.add(dizimista)
    db_session.commit()

    response = client.get("/api/reports/aniversariantes?periodo=hoje", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert any(a["nome"] == "Aniversariante Hoje" for a in data)


def test_get_aniversariantes_mes(client, auth_headers, db_session, sample_comunidade):
    """Testa relatório de aniversariantes do mês."""
    from app.models.dizimista import Dizimista

    hoje = date.today()
    dizimista = Dizimista(
        nome="Aniversariante Mês",
        comunidade_id=sample_comunidade.id,
        data_nascimento=date(1990, hoje.month, 15),
        ativo=True
    )
    db_session.add(dizimista)
    db_session.commit()

    response = client.get("/api/reports/aniversariantes?periodo=mes", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)


def test_get_total_periodo(client, auth_headers, db_session, sample_dizimista, sample_comunidade):
    """Testa relatório de total por período."""
    from app.models.contribuicao import Contribuicao, TipoContribuicaoEnum

    hoje = date.today()
    contrib1 = Contribuicao(
        dizimista_id=sample_dizimista.id,
        comunidade_id=sample_comunidade.id,
        tipo=TipoContribuicaoEnum.DIZIMO,
        valor=Decimal("100.00"),
        data_contribuicao=hoje
    )
    contrib2 = Contribuicao(
        dizimista_id=sample_dizimista.id,
        comunidade_id=sample_comunidade.id,
        tipo=TipoContribuicaoEnum.OFERTA,
        valor=Decimal("50.00"),
        data_contribuicao=hoje
    )
    db_session.add_all([contrib1, contrib2])
    db_session.commit()

    inicio = hoje - timedelta(days=7)
    fim = hoje

    response = client.get(
        f"/api/reports/total-periodo?start_date={inicio}&end_date={fim}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "total" in data
    assert "quantidade" in data
    assert float(data["total"]) >= 150.00


def test_get_total_periodo_invalid_dates(client, auth_headers):
    """Testa validação de datas no relatório de período."""
    hoje = date.today()
    inicio = hoje
    fim = hoje - timedelta(days=7)

    response = client.get(
        f"/api/reports/total-periodo?start_date={inicio}&end_date={fim}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_total_tipo(client, auth_headers, db_session, sample_dizimista, sample_comunidade):
    """Testa relatório de total por tipo."""
    from app.models.contribuicao import Contribuicao, TipoContribuicaoEnum

    hoje = date.today()
    contrib1 = Contribuicao(
        dizimista_id=sample_dizimista.id,
        comunidade_id=sample_comunidade.id,
        tipo=TipoContribuicaoEnum.DIZIMO,
        valor=Decimal("200.00"),
        data_contribuicao=hoje
    )
    contrib2 = Contribuicao(
        dizimista_id=sample_dizimista.id,
        comunidade_id=sample_comunidade.id,
        tipo=TipoContribuicaoEnum.OFERTA,
        valor=Decimal("50.00"),
        data_contribuicao=hoje
    )
    db_session.add_all([contrib1, contrib2])
    db_session.commit()

    inicio = hoje - timedelta(days=7)
    fim = hoje

    response = client.get(
        f"/api/reports/total-tipo?start_date={inicio}&end_date={fim}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "totais" in data
    assert len(data["totais"]) > 0


def test_get_dizimista_historico(client, auth_headers, db_session, sample_dizimista, sample_comunidade):
    """Testa histórico de contribuições do dizimista."""
    from app.models.contribuicao import Contribuicao, TipoContribuicaoEnum

    contrib = Contribuicao(
        dizimista_id=sample_dizimista.id,
        comunidade_id=sample_comunidade.id,
        tipo=TipoContribuicaoEnum.DIZIMO,
        valor=Decimal("150.00"),
        data_contribuicao=date.today()
    )
    db_session.add(contrib)
    db_session.commit()

    response = client.get(
        f"/api/reports/dizimista/{sample_dizimista.id}/historico",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["dizimista_id"] == sample_dizimista.id
    assert "total_geral" in data
    assert "quantidade_total" in data
    assert "contribuicoes" in data


def test_get_dizimista_historico_not_found(client, auth_headers):
    """Testa histórico de dizimista inexistente."""
    response = client.get("/api/reports/dizimista/999999/historico", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
