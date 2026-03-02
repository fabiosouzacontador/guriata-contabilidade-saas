from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.database import Base, engine
from app import models

# Criar tabelas
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

try:
    from app.routes import auth
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
except ImportError as e:
    print(f"Warning: {e}")

try:
    from app.routes import lancamentos
    app.include_router(lancamentos.router, prefix="/api", tags=["lancamentos"])
except ImportError as e:
    print(f"Warning: {e}")

try:
    from app.routes import escolas
    app.include_router(escolas.router, prefix="/api", tags=["escolas"])
except ImportError as e:
    print(f"Warning: {e}")

try:
    from app.routes import turmas
    app.include_router(turmas.router, prefix="/api", tags=["turmas"])
except ImportError as e:
    print(f"Warning: {e}")

try:
    from app.routes import ia_tutor
    app.include_router(ia_tutor.router, prefix="/api/ia-tutor", tags=["ia-tutor"])
except ImportError as e:
    print(f"Warning: {e}")

@app.get("/")
def read_root():
    return {
        "message": "Guriata Backend Running",
        "version": "1.0.0",
        "docs": "http://localhost:8000/docs"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
