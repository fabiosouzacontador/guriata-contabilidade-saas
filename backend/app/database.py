"""
Configuração do banco de dados com SQLAlchemy.

Suporta:
  - SQLite   (desenvolvimento local — sem instalação extra)
  - PostgreSQL (produção — Neon, Supabase, Railway…)

Para trocar de banco, basta alterar a variável DATABASE_URL no arquivo .env.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# URL de conexão: lida do ambiente, com SQLite como padrão para desenvolvimento
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./guriata.db")

# SQLite precisa de check_same_thread=False para funcionar com FastAPI (async)
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL: pool de conexões para melhor performance em produção
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,   # verifica conexões inativas antes de usar
        pool_size=5,
        max_overflow=10,
    )

# Fábrica de sessões — cada request recebe sua própria sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para todos os modelos SQLAlchemy (User, Escola, Turma…)
Base = declarative_base()


def get_db():
    """
    Dependência FastAPI que fornece uma sessão de banco por request.

    Uso nos endpoints:
        @router.get("/items")
        def list_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
