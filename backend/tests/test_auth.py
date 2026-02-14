"""
Testes para autenticação e autorização.
"""
import pytest
from fastapi import status


def test_login_success(client, admin_user):
    """Testa login bem-sucedido."""
    response = client.post(
        "/api/auth/login",
        json={"email": "admin_test@ecclesia.com", "senha": "Admin123!"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client, admin_user):
    """Testa login com credenciais inválidas."""
    response = client.post(
        "/api/auth/login",
        json={"email": "admin_test@ecclesia.com", "senha": "WrongPassword"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_inactive_user(client, db_session, admin_user):
    """Testa login com usuário inativo."""
    admin_user.ativo = False
    db_session.commit()

    response = client.post(
        "/api/auth/login",
        json={"email": "admin_test@ecclesia.com", "senha": "Admin123!"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_current_user(client, auth_headers):
    """Testa obtenção de dados do usuário autenticado."""
    response = client.get("/api/auth/me", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "admin_test@ecclesia.com"
    assert data["role"] == "ADMIN"


def test_get_current_user_unauthorized(client):
    """Testa acesso sem autenticação."""
    response = client.get("/api/auth/me")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_register_admin_only(client, auth_headers, operador_user):
    """Testa que apenas admin pode registrar usuários."""
    from app.auth.utils import create_access_token

    # Token de operador
    operador_token = create_access_token(
        data={"sub": operador_user.email, "user_id": operador_user.id}
    )

    response = client.post(
        "/api/auth/register",
        headers={"Authorization": f"Bearer {operador_token}"},
        json={
            "nome": "Novo Usuário",
            "email": "novo@ecclesia.com",
            "senha": "Senha123!",
            "role": "OPERADOR"
        }
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_register_success(client, auth_headers):
    """Testa registro de novo usuário por admin."""
    response = client.post(
        "/api/auth/register",
        headers=auth_headers,
        json={
            "nome": "Novo Usuário",
            "email": "novo@ecclesia.com",
            "senha": "Senha123!",
            "role": "OPERADOR"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "novo@ecclesia.com"
    assert data["role"] == "OPERADOR"


def test_register_duplicate_email(client, auth_headers, admin_user):
    """Testa registro com email duplicado."""
    response = client.post(
        "/api/auth/register",
        headers=auth_headers,
        json={
            "nome": "Outro Nome",
            "email": "admin_test@ecclesia.com",
            "senha": "Senha123!",
            "role": "OPERADOR"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
