from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/api/lancamentos", tags=["lancamentos"])

# ============================================
# CREATE
# ============================================

@router.post("/", response_model=schemas.LancamentoResponse, status_code=status.HTTP_201_CREATED)
async def create_lancamento(lancamento: schemas.LancamentoCreate, usuario_id: int, db: Session = Depends(get_db)):
    """Criar novo lançamento contábil"""
    # Verificar se usuário existe
    usuario = db.query(models.User).filter(models.User.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Verificar se contas existem
    conta_debito = db.query(models.Conta).filter(models.Conta.id == lancamento.conta_debito_id).first()
    if not conta_debito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta débito não encontrada"
        )
    
    conta_credito = db.query(models.Conta).filter(models.Conta.id == lancamento.conta_credito_id).first()
    if not conta_credito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta crédito não encontrada"
        )
    
    # Verificar se turma existe (se fornecida)
    if lancamento.turma_id:
        turma = db.query(models.Turma).filter(models.Turma.id == lancamento.turma_id).first()
        if not turma:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Turma não encontrada"
            )
    
    db_lancamento = models.Lancamento(
        **lancamento.dict(),
        usuario_id=usuario_id,
        data_lancamento=datetime.now()
    )
    
    # Atualizar saldos das contas
    conta_debito.saldo_atual += lancamento.valor
    conta_credito.saldo_atual -= lancamento.valor
    
    db.add(db_lancamento)
    db.add(conta_debito)
    db.add(conta_credito)
    db.commit()
    db.refresh(db_lancamento)
    return db_lancamento

# ============================================
# READ
# ============================================

@router.get("/", response_model=list[schemas.LancamentoResponse])
async def list_lancamentos(turma_id: int = None, conta_id: int = None, status: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar lançamentos (opcionalmente filtrar)"""
    query = db.query(models.Lancamento)
    
    if turma_id:
        query = query.filter(models.Lancamento.turma_id == turma_id)
    
    if conta_id:
        query = query.filter(
            (models.Lancamento.conta_debito_id == conta_id) |
            (models.Lancamento.conta_credito_id == conta_id)
        )
    
    if status:
        query = query.filter(models.Lancamento.status == status)
    
    lancamentos = query.offset(skip).limit(limit).all()
    return lancamentos

@router.get("/{lancamento_id}", response_model=schemas.LancamentoResponse)
async def get_lancamento(lancamento_id: int, db: Session = Depends(get_db)):
    """Obter lançamento específico"""
    lancamento = db.query(models.Lancamento).filter(models.Lancamento.id == lancamento_id).first()
    if not lancamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lançamento não encontrado"
        )
    return lancamento

# ============================================
# UPDATE
# ============================================

@router.put("/{lancamento_id}", response_model=schemas.LancamentoResponse)
async def update_lancamento(lancamento_id: int, lancamento: schemas.LancamentoUpdate, db: Session = Depends(get_db)):
    """Atualizar lançamento"""
    db_lancamento = db.query(models.Lancamento).filter(models.Lancamento.id == lancamento_id).first()
    if not db_lancamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lançamento não encontrado"
        )
    
    update_data = lancamento.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_lancamento, field, value)
    
    db.add(db_lancamento)
    db.commit()
    db.refresh(db_lancamento)
    return db_lancamento

# ============================================
# DELETE
# ============================================

@router.delete("/{lancamento_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lancamento(lancamento_id: int, db: Session = Depends(get_db)):
    """Deletar lançamento"""
    db_lancamento = db.query(models.Lancamento).filter(models.Lancamento.id == lancamento_id).first()
    if not db_lancamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lançamento não encontrado"
        )
    
    # Reverter saldos
    conta_debito = db.query(models.Conta).filter(models.Conta.id == db_lancamento.conta_debito_id).first()
    conta_credito = db.query(models.Conta).filter(models.Conta.id == db_lancamento.conta_credito_id).first()
    
    conta_debito.saldo_atual -= db_lancamento.valor
    conta_credito.saldo_atual += db_lancamento.valor
    
    db.add(conta_debito)
    db.add(conta_credito)
    db.delete(db_lancamento)
    db.commit()
    return None
