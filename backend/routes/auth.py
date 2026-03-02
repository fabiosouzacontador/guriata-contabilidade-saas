from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.post("/register")
async def register(email: str, password: str, name: str, db: Session = Depends(get_db)):
    return {"message": "User registered successfully"}

@router.post("/login")
async def login(email: str, password: str, db: Session = Depends(get_db)):
    return {"access_token": "token", "token_type": "bearer"}
