"""
Router de Autenticação.
Endpoints para login, registro e informações do usuário.
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.database import get_db
from app.schemas.auth import Login, Token
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.models.usuario import Usuario
from app.services.auth_service import authenticate_user, create_user
from app.auth.dependencies import get_current_active_user, require_admin
from app.auth.utils import create_access_token
from app.config import settings

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login(request: Request, login_data: Login, db: Session = Depends(get_db)):
    """
    Autentica um usuário e retorna um token JWT.
    Rate limit: 5 tentativas por minuto por IP.

    Args:
        request: Request object para rate limiting
        login_data: Credenciais de login (email e senha)
        db: Sessão do banco de dados

    Returns:
        Token de acesso JWT

    Raises:
        HTTPException: Se as credenciais forem inválidas
    """
    user = authenticate_user(db, login_data.email, login_data.senha)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.ativo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def register(
    request: Request,
    user_data: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """
    Registra um novo usuário (apenas administradores).
    Rate limit: 10 registros por minuto por IP.

    Args:
        request: Request object para rate limiting
        user_data: Dados do novo usuário
        db: Sessão do banco de dados
        current_user: Usuário autenticado (deve ser admin)

    Returns:
        Usuário criado

    Raises:
        HTTPException: Se o email já estiver em uso
    """
    try:
        user = create_user(db, user_data)
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado no sistema"
        )


@router.get("/me", response_model=UsuarioResponse)
async def get_current_user_info(current_user: Usuario = Depends(get_current_active_user)):
    """
    Obtém informações do usuário autenticado.

    Args:
        current_user: Usuário autenticado

    Returns:
        Informações do usuário
    """
    return current_user
