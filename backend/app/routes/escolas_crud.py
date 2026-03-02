from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/api/escolas", tags=["escolas"])

# ============================================
# CREATE
# ============================================

@router.post("/", response_model=schemas.EscolaResponse, status_code=status.HTTP_201_CREATED)
async def create_escola(escola: schemas.EscolaCreate, criador_id: int, db: Session = Depends(get_db)):
    """Criar nova escola"""
    # Verificar se usuário existe
    user = db.query(models.User).filter(models.User.id == criador_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    db_escola = models.Escola(
        **escola.dict(),
        criador_id=criador_id
    )
    db.add(db_escola)
    db.commit()
    db.refresh(db_escola)
    return db_escola

# ============================================
# READ
# ============================================

@router.get("/", response_model=list[schemas.EscolaResponse])
async def list_escolas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todas as escolas"""
    escolas = db.query(models.Escola).offset(skip).limit(limit).all()
    return escolas

@router.get("/{escola_id}", response_model=schemas.EscolaResponse)
async def get_escola(escola_id: int, db: Session = Depends(get_db)):
    """Obter escola específica"""
    escola = db.query(models.Escola).filter(models.Escola.id == escola_id).first()
    if not escola:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Escola não encontrada"
        )
    return escola

# ============================================
# UPDATE
# ============================================

@router.put("/{escola_id}", response_model=schemas.EscolaResponse)
async def update_escola(escola_id: int, escola: schemas.EscolaUpdate, db: Session = Depends(get_db)):
    """Atualizar escola"""
    db_escola = db.query(models.Escola).filter(models.Escola.id == escola_id).first()
    if not db_escola:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Escola não encontrada"
        )
    
    update_data = escola.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_escola, field, value)
    
    db.add(db_escola)
    db.commit()
    db.refresh(db_escola)
    return db_escola

# ============================================
# DELETE
# ============================================

@router.delete("/{escola_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_escola(escola_id: int, db: Session = Depends(get_db)):
    """Deletar escola"""
    db_escola = db.query(models.Escola).filter(models.Escola.id == escola_id).first()
    if not db_escola:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Escola não encontrada"
        )
    
    db.delete(db_escola)
    db.commit()
    return None
