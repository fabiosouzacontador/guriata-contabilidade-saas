from fastapi import FastAPI

from app.routers import auth

app = FastAPI(title="Guriata Contabilidade")

app.include_router(auth.router)