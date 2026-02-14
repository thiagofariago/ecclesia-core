"""
Testes para operações CRUD de Paróquias.
"""
import pytest
from fastapi import status


def test_create_paroquia(client, auth_headers):
    """Testa criação de paróquia."""
    response = client.post(
        "/api/paroquias",
        headers=auth_headers,
        json={"nome": "Paróquia Nova"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["nome"] == "Paróquia Nova"
    assert "id" in data


def test_list_paroquias(client, auth_headers, sample_paroquia):
    """Testa listagem de paróquias."""
    response = client.get("/api/paroquias", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_paroquia(client, auth_headers, sample_paroquia):
    """Testa obtenção de paróquia por ID."""
    response = client.get(f"/api/paroquias/{sample_paroquia.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == sample_paroquia.id
    assert data["nome"] == sample_paroquia.nome


def test_get_paroquia_not_found(client, auth_headers):
    """Testa obtenção de paróquia inexistente."""
    response = client.get("/api/paroquias/999999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_paroquia(client, auth_headers, sample_paroquia):
    """Testa atualização de paróquia."""
    response = client.patch(
        f"/api/paroquias/{sample_paroquia.id}",
        headers=auth_headers,
        json={"nome": "Paróquia Atualizada"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["nome"] == "Paróquia Atualizada"


def test_delete_paroquia(client, auth_headers, db_session):
    """Testa deleção de paróquia."""
    from app.models.paroquia import Paroquia

    paroquia = Paroquia(nome="Paróquia para Deletar")
    db_session.add(paroquia)
    db_session.commit()
    db_session.refresh(paroquia)

    response = client.delete(f"/api/paroquias/{paroquia.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_paroquia_with_comunidades(client, auth_headers, sample_paroquia, sample_comunidade):
    """Testa que não é possível deletar paróquia com comunidades."""
    response = client.delete(f"/api/paroquias/{sample_paroquia.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
