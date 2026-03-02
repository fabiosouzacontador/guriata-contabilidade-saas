from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.post("/feedback")
async def get_ia_feedback(lancamento_id: int, user_id: int, db: Session = Depends(get_db)):
    return {"message": "Feedback provided", "score": 100}

@router.get("/hints/{topico}")
async def get_ia_hints(topico: str, db: Session = Depends(get_db)):
    return {"topico": topico, "hint": "Remember debits and credits must balance"}
