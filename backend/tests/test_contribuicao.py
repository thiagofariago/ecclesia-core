"""
Testes para operações CRUD de Contribuições.
"""
import pytest
from fastapi import status
from datetime import date
from decimal import Decimal


def test_create_contribuicao(client, auth_headers, sample_dizimista, sample_comunidade):
    """Testa criação de contribuição."""
    response = client.post(
        "/api/contribuicoes",
        headers=auth_headers,
        json={
            "dizimista_id": sample_dizimista.id,
            "comunidade_id": sample_comunidade.id,
            "tipo": "DIZIMO",
            "valor": "150.00",
            "data_contribuicao": str(date.today()),
            "forma_pagamento": "PIX",
            "referencia_mes": date.today().strftime("%Y-%m")
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["tipo"] == "DIZIMO"
    assert float(data["valor"]) == 150.00


def test_create_contribuicao_valor_zero(client, auth_headers, sample_comunidade):
    """Testa validação de valor maior que zero."""
    response = client.post(
        "/api/contribuicoes",
        headers=auth_headers,
        json={
            "comunidade_id": sample_comunidade.id,
            "tipo": "OFERTA",
            "valor": "0",
            "data_contribuicao": str(date.today())
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_contribuicao_anonima(client, auth_headers, sample_comunidade):
    """Testa criação de contribuição anônima."""
    response = client.post(
        "/api/contribuicoes",
        headers=auth_headers,
        json={
            "dizimista_id": None,
            "comunidade_id": sample_comunidade.id,
            "tipo": "OFERTA",
            "valor": "50.00",
            "data_contribuicao": str(date.today())
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["dizimista_id"] is None


def test_list_contribuicoes(client, auth_headers, db_session, sample_dizimista, sample_comunidade):
    """Testa listagem paginada de contribuições."""
    from app.models.contribuicao import Contribuicao, TipoContribuicaoEnum

    # Criar algumas contribuições
    contrib = Contribuicao(
        dizimista_id=sample_dizimista.id,
        comunidade_id=sample_comunidade.id,
        tipo=TipoContribuicaoEnum.DIZIMO,
        valor=Decimal("100.00"),
        data_contribuicao=date.today()
    )
    db_session.add(contrib)
    db_session.commit()

    response = client.get("/api/contribuicoes", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert "total" in data


def test_list_contribuicoes_by_dizimista(client, auth_headers, db_session, sample_dizimista, sample_comunidade):
    """Testa filtro por dizimista."""
    from app.models.contribuicao import Contribuicao, TipoContribuicaoEnum

    contrib = Contribuicao(
        dizimista_id=sample_dizimista.id,
        comunidade_id=sample_comunidade.id,
        tipo=TipoContribuicaoEnum.DIZIMO,
        valor=Decimal("100.00"),
        data_contribuicao=date.today()
    )
    db_session.add(contrib)
    db_session.commit()

    response = client.get(
        f"/api/contribuicoes?dizimista_id={sample_dizimista.id}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(c["dizimista_id"] == sample_dizimista.id for c in data["items"] if c["dizimista_id"])


def test_list_contribuicoes_by_tipo(client, auth_headers, db_session, sample_dizimista, sample_comunidade):
    """Testa filtro por tipo."""
    from app.models.contribuicao import Contribuicao, TipoContribuicaoEnum

    contrib = Contribuicao(
        dizimista_id=sample_dizimista.id,
        comunidade_id=sample_comunidade.id,
        tipo=TipoContribuicaoEnum.OFERTA,
        valor=Decimal("50.00"),
        data_contribuicao=date.today()
    )
    db_session.add(contrib)
    db_session.commit()

    response = client.get("/api/contribuicoes?tipo=OFERTA", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(c["tipo"] == "OFERTA" for c in data["items"])


def test_get_contribuicao(client, auth_headers, db_session, sample_dizimista, sample_comunidade):
    """Testa obtenção de contribuição por ID."""
    from app.models.contribuicao import Contribuicao, TipoContribuicaoEnum

    contrib = Contribuicao(
        dizimista_id=sample_dizimista.id,
        comunidade_id=sample_comunidade.id,
        tipo=TipoContribuicaoEnum.DIZIMO,
        valor=Decimal("100.00"),
        data_contribuicao=date.today()
    )
    db_session.add(contrib)
    db_session.commit()
    db_session.refresh(contrib)

    response = client.get(f"/api/contribuicoes/{contrib.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == contrib.id


def test_update_contribuicao(client, auth_headers, db_session, sample_dizimista, sample_comunidade):
    """Testa atualização de contribuição."""
    from app.models.contribuicao import Contribuicao, TipoContribuicaoEnum

    contrib = Contribuicao(
        dizimista_id=sample_dizimista.id,
        comunidade_id=sample_comunidade.id,
        tipo=TipoContribuicaoEnum.DIZIMO,
        valor=Decimal("100.00"),
        data_contribuicao=date.today()
    )
    db_session.add(contrib)
    db_session.commit()
    db_session.refresh(contrib)

    response = client.patch(
        f"/api/contribuicoes/{contrib.id}",
        headers=auth_headers,
        json={"valor": "200.00"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert float(data["valor"]) == 200.00


def test_delete_contribuicao(client, auth_headers, db_session, sample_dizimista, sample_comunidade):
    """Testa deleção de contribuição."""
    from app.models.contribuicao import Contribuicao, TipoContribuicaoEnum

    contrib = Contribuicao(
        dizimista_id=sample_dizimista.id,
        comunidade_id=sample_comunidade.id,
        tipo=TipoContribuicaoEnum.DIZIMO,
        valor=Decimal("100.00"),
        data_contribuicao=date.today()
    )
    db_session.add(contrib)
    db_session.commit()
    db_session.refresh(contrib)

    response = client.delete(f"/api/contribuicoes/{contrib.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
