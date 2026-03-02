from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.get("/lancamentos")
async def list_lancamentos(db: Session = Depends(get_db)):
    return {"lancamentos": [], "total": 0}

@router.post("/lancamentos")
async def create_lancamento(conta_debito: str, conta_credito: str, valor: float, db: Session = Depends(get_db)):
    return {"message": "Lancamento created"}
