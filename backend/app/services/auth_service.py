"""
Serviço de autenticação.
Lógica de negócio para autenticação de usuários.
"""
from typing import Optional
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from app.auth.utils import verify_password, get_password_hash


def authenticate_user(db: Session, email: str, password: str) -> Optional[Usuario]:
    """
    Autentica um usuário.

    Args:
        db: Sessão do banco de dados
        email: Email do usuário
        password: Senha do usuário

    Returns:
        Usuário autenticado ou None se credenciais inválidas
    """
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.senha_hash):
        return None
    return user


def create_user(db: Session, user_data: UsuarioCreate) -> Usuario:
    """
    Cria um novo usuário.

    Args:
        db: Sessão do banco de dados
        user_data: Dados do usuário a ser criado

    Returns:
        Usuário criado
    """
    senha_hash = get_password_hash(user_data.senha)
    db_user = Usuario(
        nome=user_data.nome,
        email=user_data.email,
        senha_hash=senha_hash,
        role=user_data.role,
        ativo=user_data.ativo,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
