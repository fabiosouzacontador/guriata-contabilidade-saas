from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/api/alunos", tags=["alunos"])

# ============================================
# CREATE
# ============================================

@router.post("/", response_model=schemas.AlunoResponse, status_code=status.HTTP_201_CREATED)
async def create_aluno(aluno: schemas.AlunoCreate, db: Session = Depends(get_db)):
    """Criar novo aluno"""
    # Verificar se turma existe
    turma = db.query(models.Turma).filter(models.Turma.id == aluno.turma_id).first()
    if not turma:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Turma não encontrada"
        )
    
    db_aluno = models.Aluno(**aluno.dict())
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

# ============================================
# READ
# ============================================

@router.get("/", response_model=list[schemas.AlunoResponse])
async def list_alunos(turma_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar alunos (opcionalmente filtrar por turma)"""
    query = db.query(models.Aluno)
    if turma_id:
        query = query.filter(models.Aluno.turma_id == turma_id)
    
    alunos = query.offset(skip).limit(limit).all()
    return alunos

@router.get("/{aluno_id}", response_model=schemas.AlunoResponse)
async def get_aluno(aluno_id: int, db: Session = Depends(get_db)):
    """Obter aluno específico"""
    aluno = db.query(models.Aluno).filter(models.Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )
    return aluno

@router.get("/matricula/{matricula}", response_model=schemas.AlunoResponse)
async def get_aluno_by_matricula(matricula: str, db: Session = Depends(get_db)):
    """Obter aluno por matrícula"""
    aluno = db.query(models.Aluno).filter(models.Aluno.matricula == matricula).first()
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )
    return aluno

# ============================================
# UPDATE
# ============================================

@router.put("/{aluno_id}", response_model=schemas.AlunoResponse)
async def update_aluno(aluno_id: int, aluno: schemas.AlunoUpdate, db: Session = Depends(get_db)):
    """Atualizar aluno"""
    db_aluno = db.query(models.Aluno).filter(models.Aluno.id == aluno_id).first()
    if not db_aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )
    
    update_data = aluno.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_aluno, field, value)
    
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

# ============================================
# DELETE
# ============================================

@router.delete("/{aluno_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_aluno(aluno_id: int, db: Session = Depends(get_db)):
    """Deletar aluno"""
    db_aluno = db.query(models.Aluno).filter(models.Aluno.id == aluno_id).first()
    if not db_aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )
    
    db.delete(db_aluno)
    db.commit()
    return None
