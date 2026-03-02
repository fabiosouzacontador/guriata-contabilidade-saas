from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.get("/escolas")
async def list_escolas(db: Session = Depends(get_db)):
    return {"escolas": [], "total": 0}

@router.post("/escolas")
async def create_escola(nome: str, localizacao: str, db: Session = Depends(get_db)):
    return {"message": "Escola created successfully"}
