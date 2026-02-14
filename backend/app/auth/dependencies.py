"""
Dependencies para autenticação e autorização.
Funções de dependency injection para FastAPI.
"""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario, RoleEnum
from app.auth.utils import decode_access_token

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Obtém o usuário atual a partir do token JWT.

    Args:
        credentials: Credenciais HTTP Bearer
        db: Sessão do banco de dados

    Returns:
        Usuário autenticado

    Raises:
        HTTPException: Se o token for inválido ou o usuário não existir
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise credentials_exception

    email: Optional[str] = payload.get("sub")
    if email is None:
        raise credentials_exception

    user = db.query(Usuario).filter(Usuario.email == email).first()
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """
    Obtém o usuário atual e verifica se está ativo.

    Args:
        current_user: Usuário autenticado

    Returns:
        Usuário ativo

    Raises:
        HTTPException: Se o usuário estiver inativo
    """
    if not current_user.ativo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )
    return current_user


def require_role(required_role: RoleEnum):
    """
    Cria uma dependency que verifica se o usuário tem o papel necessário.

    Args:
        required_role: Papel requerido

    Returns:
        Função de dependency
    """
    async def role_checker(current_user: Usuario = Depends(get_current_active_user)) -> Usuario:
        """
        Verifica se o usuário tem o papel necessário.

        Args:
            current_user: Usuário autenticado e ativo

        Returns:
            Usuário com papel adequado

        Raises:
            HTTPException: Se o usuário não tiver o papel necessário
        """
        if current_user.role != required_role and current_user.role != RoleEnum.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permissões insuficientes para esta operação"
            )
        return current_user

    return role_checker


async def require_admin(current_user: Usuario = Depends(get_current_active_user)) -> Usuario:
    """
    Verifica se o usuário é administrador.

    Args:
        current_user: Usuário autenticado e ativo

    Returns:
        Usuário administrador

    Raises:
        HTTPException: Se o usuário não for administrador
    """
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem realizar esta operação"
        )
    return current_user
