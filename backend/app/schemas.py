from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum

# ============================================
# ENUMS (para Pydantic)
# ============================================

class TipoConta(str, Enum):
    ATIVO = "ATIVO"
    PASSIVO = "PASSIVO"
    PATRIMONIO = "PATRIMONIO"
    RECEITA = "RECEITA"
    DESPESA = "DESPESA"

class StatusLancamento(str, Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    REJEITADO = "REJEITADO"

class StatusAluno(str, Enum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"
    SUSPENSO = "SUSPENSO"

# ============================================
# USER SCHEMAS
# ============================================

class UserBase(BaseModel):
    email: EmailStr
    nome: str
    eh_professor: bool = False
    eh_admin: bool = False

class UserCreate(UserBase):
    senha: str

class UserUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    eh_professor: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    ativo: bool
    criado_em: datetime
    atualizado_em: Optional[datetime]

    class Config:
        from_attributes = True

# ============================================
# ESCOLA SCHEMAS
# ============================================

class EscolaBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    cnpj: Optional[str] = None
    endereco: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None

class EscolaCreate(EscolaBase):
    pass

class EscolaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None

class EscolaResponse(EscolaBase):
    id: int
    criador_id: int
    ativa: bool
    criado_em: datetime
    atualizado_em: Optional[datetime]

    class Config:
        from_attributes = True

# ============================================
# TURMA SCHEMAS
# ============================================

class TurmaBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    periodo: Optional[str] = None
    escola_id: int
    professor_id: int

class TurmaCreate(TurmaBase):
    pass

class TurmaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    periodo: Optional[str] = None

class TurmaResponse(TurmaBase):
    id: int
    ativa: bool
    criado_em: datetime
    atualizado_em: Optional[datetime]

    class Config:
        from_attributes = True

# ============================================
# ALUNO SCHEMAS
# ============================================

class AlunoBase(BaseModel):
    matricula: str
    nome: str
    email: Optional[str] = None
    cpf: Optional[str] = None
    turma_id: int

class AlunoCreate(AlunoBase):
    pass

class AlunoUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    status: Optional[StatusAluno] = None

class AlunoResponse(AlunoBase):
    id: int
    status: StatusAluno
    criado_em: datetime
    atualizado_em: Optional[datetime]

    class Config:
        from_attributes = True

# ============================================
# CONTA SCHEMAS
# ============================================

class ContaBase(BaseModel):
    codigo: str
    nome: str
    descricao: Optional[str] = None
    tipo: TipoConta
    saldo_inicial: float = 0.0
    escola_id: int
    conta_pai_id: Optional[int] = None

class ContaCreate(ContaBase):
    pass

class ContaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    saldo_inicial: Optional[float] = None

class ContaResponse(ContaBase):
    id: int
    saldo_atual: float
    ativa: bool
    criado_em: datetime
    atualizado_em: Optional[datetime]

    class Config:
        from_attributes = True

# ============================================
# LANCAMENTO SCHEMAS
# ============================================

class LancamentoBase(BaseModel):
    numero: str
    descricao: str
    valor: float
    conta_debito_id: int
    conta_credito_id: int
    turma_id: Optional[int] = None
    data_vencimento: Optional[datetime] = None
    observacoes: Optional[str] = None

class LancamentoCreate(LancamentoBase):
    pass

class LancamentoUpdate(BaseModel):
    descricao: Optional[str] = None
    status: Optional[StatusLancamento] = None
    observacoes: Optional[str] = None

class LancamentoResponse(LancamentoBase):
    id: int
    usuario_id: int
    status: StatusLancamento
    data_lancamento: datetime
    criado_em: datetime
    atualizado_em: Optional[datetime]

    class Config:
        from_attributes = True

# ============================================
# FEEDBACK IA SCHEMAS
# ============================================

class FeedbackIABase(BaseModel):
    lancamento_id: int
    tipo_feedback: str
    mensagem: str
    score: int = 0

class FeedbackIACreate(FeedbackIABase):
    pass

class FeedbackIAResponse(FeedbackIABase):
    id: int
    usuario_id: int
    eh_correto: Optional[bool]
    explicacao: Optional[str]
    dicas: Optional[str]
    criado_em: datetime

    class Config:
        from_attributes = True
