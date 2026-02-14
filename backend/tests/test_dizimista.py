"""
Testes para operações CRUD de Dizimistas.
"""
import pytest
from fastapi import status
from datetime import date


def test_create_dizimista(client, auth_headers, sample_comunidade):
    """Testa criação de dizimista."""
    response = client.post(
        "/api/dizimistas",
        headers=auth_headers,
        json={
            "nome": "Maria Silva",
            "comunidade_id": sample_comunidade.id,
            "cpf": "987.654.321-00",
            "telefone": "(11) 88888-8888",
            "email": "maria@teste.com",
            "data_nascimento": "1985-05-15",
            "ativo": True
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["nome"] == "Maria Silva"
    assert data["cpf"] == "987.654.321-00"


def test_create_dizimista_duplicate_cpf(client, auth_headers, sample_dizimista, sample_comunidade):
    """Testa criação com CPF duplicado."""
    response = client.post(
        "/api/dizimistas",
        headers=auth_headers,
        json={
            "nome": "Outro Nome",
            "comunidade_id": sample_comunidade.id,
            "cpf": sample_dizimista.cpf,
            "ativo": True
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_list_dizimistas(client, auth_headers, sample_dizimista):
    """Testa listagem paginada de dizimistas."""
    response = client.get("/api/dizimistas", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert "total_pages" in data


def test_list_dizimistas_with_search(client, auth_headers, sample_dizimista):
    """Testa busca de dizimistas."""
    response = client.get(
        f"/api/dizimistas?search={sample_dizimista.nome.split()[0]}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) >= 1


def test_list_dizimistas_by_comunidade(client, auth_headers, sample_comunidade, sample_dizimista):
    """Testa filtro por comunidade."""
    response = client.get(
        f"/api/dizimistas?comunidade_id={sample_comunidade.id}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(d["comunidade_id"] == sample_comunidade.id for d in data["items"])


def test_list_dizimistas_by_ativo(client, auth_headers, sample_dizimista):
    """Testa filtro por status ativo."""
    response = client.get("/api/dizimistas?ativo=true", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(d["ativo"] is True for d in data["items"])


def test_get_dizimista(client, auth_headers, sample_dizimista):
    """Testa obtenção de dizimista por ID."""
    response = client.get(f"/api/dizimistas/{sample_dizimista.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == sample_dizimista.id


def test_update_dizimista(client, auth_headers, sample_dizimista):
    """Testa atualização de dizimista."""
    response = client.patch(
        f"/api/dizimistas/{sample_dizimista.id}",
        headers=auth_headers,
        json={"telefone": "(11) 77777-7777"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["telefone"] == "(11) 77777-7777"


def test_soft_delete_dizimista(client, auth_headers, sample_dizimista, db_session):
    """Testa soft delete de dizimista."""
    response = client.delete(f"/api/dizimistas/{sample_dizimista.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verificar que foi marcado como inativo
    db_session.refresh(sample_dizimista)
    assert sample_dizimista.ativo is False
