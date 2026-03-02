from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/api/turmas", tags=["turmas"])

# ============================================
# CREATE
# ============================================

@router.post("/", response_model=schemas.TurmaResponse, status_code=status.HTTP_201_CREATED)
async def create_turma(turma: schemas.TurmaCreate, db: Session = Depends(get_db)):
    """Criar nova turma"""
    # Verificar se escola existe
    escola = db.query(models.Escola).filter(models.Escola.id == turma.escola_id).first()
    if not escola:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Escola não encontrada"
        )
    
    # Verificar se professor existe
    professor = db.query(models.User).filter(models.User.id == turma.professor_id).first()
    if not professor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professor não encontrado"
        )
    
    db_turma = models.Turma(**turma.dict())
    db.add(db_turma)
    db.commit()
    db.refresh(db_turma)
    return db_turma

# ============================================
# READ
# ============================================

@router.get("/", response_model=list[schemas.TurmaResponse])
async def list_turmas(escola_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar turmas (opcionalmente filtrar por escola)"""
    query = db.query(models.Turma)
    if escola_id:
        query = query.filter(models.Turma.escola_id == escola_id)
    
    turmas = query.offset(skip).limit(limit).all()
    return turmas

@router.get("/{turma_id}", response_model=schemas.TurmaResponse)
async def get_turma(turma_id: int, db: Session = Depends(get_db)):
    """Obter turma específica"""
    turma = db.query(models.Turma).filter(models.Turma.id == turma_id).first()
    if not turma:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Turma não encontrada"
        )
    return turma

# ============================================
# UPDATE
# ============================================

@router.put("/{turma_id}", response_model=schemas.TurmaResponse)
async def update_turma(turma_id: int, turma: schemas.TurmaUpdate, db: Session = Depends(get_db)):
    """Atualizar turma"""
    db_turma = db.query(models.Turma).filter(models.Turma.id == turma_id).first()
    if not db_turma:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Turma não encontrada"
        )
    
    update_data = turma.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_turma, field, value)
    
    db.add(db_turma)
    db.commit()
    db.refresh(db_turma)
    return db_turma

# ============================================
# DELETE
# ============================================

@router.delete("/{turma_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_turma(turma_id: int, db: Session = Depends(get_db)):
    """Deletar turma"""
    db_turma = db.query(models.Turma).filter(models.Turma.id == turma_id).first()
    if not db_turma:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Turma não encontrada"
        )
    
    db.delete(db_turma)
    db.commit()
    return None
