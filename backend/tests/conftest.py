"""
Configuração do pytest e fixtures compartilhadas.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

# Database de teste em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    """
    Fixture que cria um banco de dados de teste e retorna uma sessão.
    Após cada teste, faz rollback das alterações.
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    """
    Fixture que retorna um TestClient do FastAPI com banco de dados de teste.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    """
    Fixture com dados de usuário para testes.
    """
    return {
        "email": "test@ecclesia.com",
        "password": "TestPassword123!",
        "name": "Test User"
    }


@pytest.fixture
def admin_user(db_session):
    """
    Fixture que cria e retorna um usuário administrador.
    """
    from app.models.usuario import Usuario, RoleEnum
    from app.auth.utils import get_password_hash

    user = Usuario(
        nome="Admin Test",
        email="admin_test@ecclesia.com",
        senha_hash=get_password_hash("Admin123!"),
        role=RoleEnum.ADMIN,
        ativo=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def operador_user(db_session):
    """
    Fixture que cria e retorna um usuário operador.
    """
    from app.models.usuario import Usuario, RoleEnum
    from app.auth.utils import get_password_hash

    user = Usuario(
        nome="Operador Test",
        email="operador_test@ecclesia.com",
        senha_hash=get_password_hash("Opera123!"),
        role=RoleEnum.OPERADOR,
        ativo=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def sample_paroquia(db_session):
    """
    Fixture que cria e retorna uma paróquia de exemplo.
    """
    from app.models.paroquia import Paroquia

    paroquia = Paroquia(nome="Paróquia Teste")
    db_session.add(paroquia)
    db_session.commit()
    db_session.refresh(paroquia)
    return paroquia


@pytest.fixture
def sample_comunidade(db_session, sample_paroquia):
    """
    Fixture que cria e retorna uma comunidade de exemplo.
    """
    from app.models.comunidade import Comunidade

    comunidade = Comunidade(
        nome="Comunidade Teste",
        paroquia_id=sample_paroquia.id
    )
    db_session.add(comunidade)
    db_session.commit()
    db_session.refresh(comunidade)
    return comunidade


@pytest.fixture
def sample_dizimista(db_session, sample_comunidade):
    """
    Fixture que cria e retorna um dizimista de exemplo.
    """
    from app.models.dizimista import Dizimista
    from datetime import date

    dizimista = Dizimista(
        nome="João Teste",
        comunidade_id=sample_comunidade.id,
        cpf="123.456.789-00",
        telefone="(11) 99999-9999",
        email="joao@teste.com",
        data_nascimento=date(1990, 1, 1),
        ativo=True
    )
    db_session.add(dizimista)
    db_session.commit()
    db_session.refresh(dizimista)
    return dizimista


@pytest.fixture
def auth_headers(admin_user):
    """
    Fixture que retorna headers de autenticação com token JWT.
    """
    from app.auth.utils import create_access_token

    access_token = create_access_token(data={"sub": admin_user.email, "user_id": admin_user.id})
    return {"Authorization": f"Bearer {access_token}"}
