"""
Testes para operações CRUD de Comunidades.
"""
import pytest
from fastapi import status


def test_create_comunidade(client, auth_headers, sample_paroquia):
    """Testa criação de comunidade."""
    response = client.post(
        "/api/comunidades",
        headers=auth_headers,
        json={
            "nome": "Comunidade Nova",
            "paroquia_id": sample_paroquia.id
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["nome"] == "Comunidade Nova"
    assert data["paroquia_id"] == sample_paroquia.id


def test_list_comunidades(client, auth_headers, sample_comunidade):
    """Testa listagem de comunidades."""
    response = client.get("/api/comunidades", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_list_comunidades_by_paroquia(client, auth_headers, sample_paroquia, sample_comunidade):
    """Testa listagem de comunidades filtradas por paróquia."""
    response = client.get(
        f"/api/comunidades?paroquia_id={sample_paroquia.id}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(c["paroquia_id"] == sample_paroquia.id for c in data)


def test_get_comunidade(client, auth_headers, sample_comunidade):
    """Testa obtenção de comunidade por ID."""
    response = client.get(f"/api/comunidades/{sample_comunidade.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == sample_comunidade.id


def test_update_comunidade(client, auth_headers, sample_comunidade):
    """Testa atualização de comunidade."""
    response = client.patch(
        f"/api/comunidades/{sample_comunidade.id}",
        headers=auth_headers,
        json={"nome": "Comunidade Atualizada"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["nome"] == "Comunidade Atualizada"


def test_delete_comunidade(client, auth_headers, sample_paroquia, db_session):
    """Testa deleção de comunidade."""
    from app.models.comunidade import Comunidade

    comunidade = Comunidade(
        nome="Comunidade para Deletar",
        paroquia_id=sample_paroquia.id
    )
    db_session.add(comunidade)
    db_session.commit()
    db_session.refresh(comunidade)

    response = client.delete(f"/api/comunidades/{comunidade.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_comunidade_with_dizimistas(client, auth_headers, sample_comunidade, sample_dizimista):
    """Testa que não é possível deletar comunidade com dizimistas."""
    response = client.delete(f"/api/comunidades/{sample_comunidade.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
