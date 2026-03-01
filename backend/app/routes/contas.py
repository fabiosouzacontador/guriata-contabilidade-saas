from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db

router = APIRouter()

class ContaCreate(BaseModel):
    descricao: str

class ContaResponse(BaseModel):
    id: int
    descricao: str

@router.post("/", response_model=ContaResponse)
async def create_conta(conta: ContaCreate, db: Session = Depends(get_db)):
    return {"id": 1, "descricao": conta.descricao}

@router.get("/", response_model=list)
async def list_contas(db: Session = Depends(get_db)):
    return []

@router.get("/{conta_id}", response_model=ContaResponse)
async def get_conta(conta_id: int, db: Session = Depends(get_db)):
    return {"id": conta_id, "descricao": "Conta"}

@router.put("/{conta_id}", response_model=ContaResponse)
async def update_conta(conta_id: int, conta: ContaCreate, db: Session = Depends(get_db)):
    return {"id": conta_id, "descricao": conta.descricao}

@router.delete("/{conta_id}")
async def delete_conta(conta_id: int, db: Session = Depends(get_db)):
    return {"detail": "Conta deleted"}