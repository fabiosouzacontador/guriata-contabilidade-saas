"""
Configurações centralizadas da aplicação Guriata.

Todas as configurações sensíveis devem vir de variáveis de ambiente.
NUNCA hardcode segredos em produção — use um arquivo .env local.

Exemplo de .env:
    JWT_SECRET_KEY=sua-chave-secreta-longa-e-aleatoria
    DATABASE_URL=postgresql://user:pass@host/db
    ACCESS_TOKEN_EXPIRE_MINUTES=30
"""
import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env (se existir)
load_dotenv()


class Settings:
    """
    Configurações da aplicação lidas do ambiente.

    Uso:
        from app.core.config import settings
        print(settings.SECRET_KEY)
    """

    # ── Banco de dados ────────────────────────────────────────────────────────
    # SQLite para desenvolvimento; PostgreSQL para produção (Neon, Supabase…)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "sqlite:///./guriata.db"
    )

    # ── JWT ───────────────────────────────────────────────────────────────────
    # Gere uma chave forte em produção:  openssl rand -hex 32
    SECRET_KEY: str = os.getenv(
        "JWT_SECRET_KEY", "change-this-secret-key-in-production"
    )
    # HS256 é seguro e simples para começar; RS256 para sistemas distribuídos
    ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    # Tempo de expiração do token de acesso (em minutos)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )

    # ── Aplicação ─────────────────────────────────────────────────────────────
    APP_NAME: str = "Guriata Contabilidade SaaS"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"


# Instância global usada em toda a aplicação
settings = Settings()
