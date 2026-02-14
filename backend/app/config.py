"""
Configurações da aplicação usando pydantic-settings.
Carrega variáveis de ambiente para configurar o sistema.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    """Configurações da aplicação carregadas do ambiente."""

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/ecclesia"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # Application
    APP_NAME: str = "Ecclesia - Sistema de Dízimo"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    @field_validator('SECRET_KEY')
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """
        Valida a SECRET_KEY para garantir segurança.

        Args:
            v: Valor da SECRET_KEY

        Returns:
            Valor validado

        Raises:
            ValueError: Se a chave for inválida ou fraca
        """
        if not v:
            raise ValueError("SECRET_KEY deve ser configurada nas variáveis de ambiente")
        if len(v) < 32:
            raise ValueError("SECRET_KEY deve ter pelo menos 32 caracteres")
        weak_keys = [
            "your-secret-key-change-in-production",
            "your-secret-key-change-this-in-production-use-openssl-rand-hex-32",
            "secret",
            "change-me",
            "secretkey",
            "12345"
        ]
        if v in weak_keys:
            raise ValueError("SECRET_KEY não pode ser um valor padrão ou fraco")
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


# Instância global das configurações
settings = Settings()
