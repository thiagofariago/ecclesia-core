"""
Aplicação principal FastAPI.
Entry point da API com configuração de CORS, routers e middleware.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.config import settings

# Criar instância do FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    description="Sistema de gerenciamento de dízimo e membros da igreja"
)

# Configurar CORS com origens específicas do ambiente
origins = settings.ALLOWED_ORIGINS.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Endpoint de health check para verificar se a API está funcionando.
    """
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


@app.get("/", tags=["Root"])
async def root():
    """
    Endpoint raiz da API.
    """
    return {
        "message": "Bem-vindo à API Ecclesia",
        "docs": "/docs",
        "health": "/health"
    }


# Importar routers
from app.routers import auth, paroquia, comunidade, dizimista, contribuicao, reports

# Registrar routers
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticação"])
app.include_router(paroquia.router, prefix="/api/paroquias", tags=["Paróquias"])
app.include_router(comunidade.router, prefix="/api/comunidades", tags=["Comunidades"])
app.include_router(dizimista.router, prefix="/api/dizimistas", tags=["Dizimistas"])
app.include_router(contribuicao.router, prefix="/api/contribuicoes", tags=["Contribuições"])
app.include_router(reports.router, prefix="/api/reports", tags=["Relatórios"])
