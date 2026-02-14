"""
Testes para endpoints principais da aplicação.
"""
import pytest
from fastapi import status


def test_health_check(client):
    """Testa o endpoint de health check."""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "ok"
    assert "app" in data
    assert "version" in data


def test_root_endpoint(client):
    """Testa o endpoint raiz."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data
    assert "docs" in data
    assert "health" in data


def test_docs_available(client):
    """Verifica se a documentação Swagger está disponível."""
    response = client.get("/docs")
    assert response.status_code == status.HTTP_200_OK


def test_redoc_available(client):
    """Verifica se a documentação ReDoc está disponível."""
    response = client.get("/redoc")
    assert response.status_code == status.HTTP_200_OK
