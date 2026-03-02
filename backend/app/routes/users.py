from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app import models, schemas
from passlib.context import CryptContext

router = APIRouter(prefix="/api/users", tags=["users"])

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ============================================
# CREATE
# ============================================

@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Criar novo usuário"""
    try:
        db_user = models.User(
            email=user.email,
            nome=user.nome,
            senha_hash=hash_password(user.senha),
            eh_professor=user.eh_professor,
            eh_admin=user.eh_admin
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já existe"
        )

# ============================================
# READ
# ============================================

@router.get("/", response_model=list[schemas.UserResponse])
async def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todos os usuários"""
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=schemas.UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Obter usuário específico"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return user

@router.get("/email/{email}", response_model=schemas.UserResponse)
async def get_user_by_email(email: str, db: Session = Depends(get_db)):
    """Obter usuário por email"""
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return user

# ============================================
# UPDATE
# ============================================

@router.put("/{user_id}", response_model=schemas.UserResponse)
async def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    """Atualizar usuário"""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    update_data = user.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ============================================
# DELETE
# ============================================

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Deletar usuário"""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    db.delete(db_user)
    db.commit()
    return None
