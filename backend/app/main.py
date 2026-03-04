from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.database import Base, engine
from app import models  # noqa: F401 — importar para registrar todos os modelos no Base

# Cria todas as tabelas no banco (sem afetar tabelas existentes)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Guriata",
    version="1.0.0",
    description="SaaS de Contabilidade com IA Tutor para Educação"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# ROUTERS
# ============================================

try:
    from app.routes import users
    app.include_router(users.router, tags=["users"])
except ImportError as e:
    print(f"Warning: {e}")

try:
    from app.routes import escolas_crud
    app.include_router(escolas_crud.router, tags=["escolas"])
except ImportError as e:
    print(f"Warning: {e}")

try:
    from app.routes import turmas_crud
    app.include_router(turmas_crud.router, tags=["turmas"])
except ImportError as e:
    print(f"Warning: {e}")

try:
    from app.routes import alunos
    app.include_router(alunos.router, tags=["alunos"])
except ImportError as e:
    print(f"Warning: {e}")

try:
    from app.routes import contas
    app.include_router(contas.router, tags=["contas"])
except ImportError as e:
    print(f"Warning: {e}")

try:
    from app.routes import lancamentos
    app.include_router(lancamentos.router, tags=["lancamentos"])
except ImportError as e:
    print(f"Warning: {e}")

try:
    from app.routers import auth as jwt_auth
    app.include_router(jwt_auth.router, prefix="/api/auth", tags=["auth"])
except ImportError as e:
    print(f"Warning: {e}")

try:
    from app.routes import ia_tutor
    app.include_router(ia_tutor.router, prefix="/api/ia-tutor", tags=["ia-tutor"])
except ImportError as e:
    print(f"Warning: {e}")

# ============================================
# HEALTH CHECK
# ============================================

@app.get("/")
def read_root():
    return {
        "message": "Guriata Backend Running",
        "version": "1.0.0",
        "docs": "http://localhost:8000/docs",
        "endpoints": {
            "users": "/api/users",
            "escolas": "/api/escolas",
            "turmas": "/api/turmas",
            "alunos": "/api/alunos",
            "contas": "/api/contas",
            "lancamentos": "/api/lancamentos"
        }
    }

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
