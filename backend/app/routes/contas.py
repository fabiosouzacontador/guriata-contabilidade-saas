from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/api/contas", tags=["contas"])

# ============================================
# CREATE
# ============================================

@router.post("/", response_model=schemas.ContaResponse, status_code=status.HTTP_201_CREATED)
async def create_conta(conta: schemas.ContaCreate, db: Session = Depends(get_db)):
    """Criar nova conta contábil"""
    # Verificar se escola existe
    escola = db.query(models.Escola).filter(models.Escola.id == conta.escola_id).first()
    if not escola:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Escola não encontrada"
        )
    
    # Se for subconta, verificar se conta pai existe
    if conta.conta_pai_id:
        conta_pai = db.query(models.Conta).filter(models.Conta.id == conta.conta_pai_id).first()
        if not conta_pai:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conta pai não encontrada"
            )
    
    db_conta = models.Conta(**conta.dict())
    db.add(db_conta)
    db.commit()
    db.refresh(db_conta)
    return db_conta

# ============================================
# READ
# ============================================

@router.get("/", response_model=list[schemas.ContaResponse])
async def list_contas(escola_id: int = None, tipo: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar contas (opcionalmente filtrar)"""
    query = db.query(models.Conta)
    
    if escola_id:
        query = query.filter(models.Conta.escola_id == escola_id)
    
    if tipo:
        query = query.filter(models.Conta.tipo == tipo)
    
    contas = query.offset(skip).limit(limit).all()
    return contas

@router.get("/{conta_id}", response_model=schemas.ContaResponse)
async def get_conta(conta_id: int, db: Session = Depends(get_db)):
    """Obter conta específica"""
    conta = db.query(models.Conta).filter(models.Conta.id == conta_id).first()
    if not conta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada"
        )
    return conta

@router.get("/codigo/{codigo}", response_model=schemas.ContaResponse)
async def get_conta_by_codigo(codigo: str, db: Session = Depends(get_db)):
    """Obter conta por código"""
    conta = db.query(models.Conta).filter(models.Conta.codigo == codigo).first()
    if not conta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada"
        )
    return conta

# ============================================
# UPDATE
# ============================================

@router.put("/{conta_id}", response_model=schemas.ContaResponse)
async def update_conta(conta_id: int, conta: schemas.ContaUpdate, db: Session = Depends(get_db)):
    """Atualizar conta"""
    db_conta = db.query(models.Conta).filter(models.Conta.id == conta_id).first()
    if not db_conta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada"
        )
    
    update_data = conta.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_conta, field, value)
    
    db.add(db_conta)
    db.commit()
    db.refresh(db_conta)
    return db_conta

# ============================================
# DELETE
# ============================================

@router.delete("/{conta_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conta(conta_id: int, db: Session = Depends(get_db)):
    """Deletar conta"""
    db_conta = db.query(models.Conta).filter(models.Conta.id == conta_id).first()
    if not db_conta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada"
        )
    
    db.delete(db_conta)
    db.commit()
    return None
