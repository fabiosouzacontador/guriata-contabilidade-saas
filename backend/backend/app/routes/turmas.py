from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.get("/turmas")
async def list_turmas(db: Session = Depends(get_db)):
    return {"turmas": [], "total": 0}
