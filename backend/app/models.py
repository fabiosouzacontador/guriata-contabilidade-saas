from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum
from datetime import datetime

# ============================================
# ENUMS
# ============================================

class TipoContaEnum(str, enum.Enum):
    ATIVO = "ATIVO"
    PASSIVO = "PASSIVO"
    PATRIMONIO = "PATRIMONIO"
    RECEITA = "RECEITA"
    DESPESA = "DESPESA"

class StatusLancamentoEnum(str, enum.Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    REJEITADO = "REJEITADO"

class StatusAlunoEnum(str, enum.Enum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"
    SUSPENSO = "SUSPENSO"

# ============================================
# MODELS
# ============================================

class User(Base):
    """Modelo de usuário do sistema"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    nome = Column(String(255), nullable=False)
    senha_hash = Column(String(255), nullable=False)
    ativo = Column(Boolean, default=True)
    eh_professor = Column(Boolean, default=False)
    eh_admin = Column(Boolean, default=False)
    
    # Timestamps
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    escolas = relationship("Escola", back_populates="criador")
    turmas = relationship("Turma", back_populates="professor")
    alunos = relationship("Aluno", back_populates="usuario")
    lancamentos = relationship("Lancamento", back_populates="usuario")

    class Config:
        from_attributes = True


class Escola(Base):
    """Modelo de escola/instituição educacional"""
    __tablename__ = "escolas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False, index=True)
    descricao = Column(Text, nullable=True)
    cnpj = Column(String(18), unique=True, nullable=True)
    endereco = Column(String(255), nullable=True)
    telefone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    
    # Foreign Keys
    criador_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Status
    ativa = Column(Boolean, default=True)
    
    # Timestamps
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    criador = relationship("User", back_populates="escolas")
    turmas = relationship("Turma", back_populates="escola", cascade="all, delete-orphan")
    contas = relationship("Conta", back_populates="escola", cascade="all, delete-orphan")

    class Config:
        from_attributes = True


class Turma(Base):
    """Modelo de turma/grupo de alunos"""
    __tablename__ = "turmas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=True)
    periodo = Column(String(50), nullable=True)  # Ex: "2024/1", "2º semestre"
    
    # Foreign Keys
    escola_id = Column(Integer, ForeignKey("escolas.id"), nullable=False)
    professor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Status
    ativa = Column(Boolean, default=True)
    
    # Timestamps
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    escola = relationship("Escola", back_populates="turmas")
    professor = relationship("User", back_populates="turmas")
    alunos = relationship("Aluno", back_populates="turma", cascade="all, delete-orphan")
    lancamentos = relationship("Lancamento", back_populates="turma")

    class Config:
        from_attributes = True


class Aluno(Base):
    """Modelo de aluno"""
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    matricula = Column(String(50), unique=True, nullable=False, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    cpf = Column(String(14), unique=True, nullable=True)
    
    # Foreign Keys
    turma_id = Column(Integer, ForeignKey("turmas.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Status
    status = Column(Enum(StatusAlunoEnum), default=StatusAlunoEnum.ATIVO)
    
    # Timestamps
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    turma = relationship("Turma", back_populates="alunos")
    usuario = relationship("User", back_populates="alunos")

    class Config:
        from_attributes = True


class Conta(Base):
    """Modelo de conta contábil (plano de contas)"""
    __tablename__ = "contas"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(20), nullable=False)  # Ex: "1.1.1.01"
    nome = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=True)
    tipo = Column(Enum(TipoContaEnum), nullable=False)
    
    # Saldo
    saldo_inicial = Column(Float, default=0.0)
    saldo_atual = Column(Float, default=0.0)
    
    # Foreign Keys
    escola_id = Column(Integer, ForeignKey("escolas.id"), nullable=False)
    conta_pai_id = Column(Integer, ForeignKey("contas.id"), nullable=True)  # Subconta
    
    # Status
    ativa = Column(Boolean, default=True)
    
    # Timestamps
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    escola = relationship("Escola", back_populates="contas")
    contas_filhas = relationship("Conta", remote_side=[conta_pai_id], backref="conta_pai")
    lancamentos_debito = relationship("Lancamento", foreign_keys="Lancamento.conta_debito_id", back_populates="conta_debito")
    lancamentos_credito = relationship("Lancamento", foreign_keys="Lancamento.conta_credito_id", back_populates="conta_credito")

    class Config:
        from_attributes = True


class Lancamento(Base):
    """Modelo de lançamento contábil"""
    __tablename__ = "lancamentos"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String(50), unique=True, nullable=False, index=True)
    descricao = Column(String(255), nullable=False)
    valor = Column(Float, nullable=False)
    
    # Foreign Keys
    conta_debito_id = Column(Integer, ForeignKey("contas.id"), nullable=False)
    conta_credito_id = Column(Integer, ForeignKey("contas.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    turma_id = Column(Integer, ForeignKey("turmas.id"), nullable=True)
    
    # Status
    status = Column(Enum(StatusLancamentoEnum), default=StatusLancamentoEnum.PENDENTE)
    
    # Data do lançamento
    data_lancamento = Column(DateTime, nullable=False, default=func.now)
    data_vencimento = Column(DateTime, nullable=True)
    
    # Observações
    observacoes = Column(Text, nullable=True)
    
    # Timestamps
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    conta_debito = relationship("Conta", foreign_keys=[conta_debito_id], back_populates="lancamentos_debito")
    conta_credito = relationship("Conta", foreign_keys=[conta_credito_id], back_populates="lancamentos_credito")
    usuario = relationship("User", back_populates="lancamentos")
    turma = relationship("Turma", back_populates="lancamentos")
    feedback = relationship("FeedbackIA", back_populates="lancamento", cascade="all, delete-orphan")

    class Config:
        from_attributes = True


class FeedbackIA(Base):
    """Modelo de feedback da IA Tutor"""
    __tablename__ = "feedback_ia"

    id = Column(Integer, primary_key=True, index=True)
    lancamento_id = Column(Integer, ForeignKey("lancamentos.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Feedback
    tipo_feedback = Column(String(50), nullable=False)  # "CORRETO", "INCORRETO", "DICA"
    mensagem = Column(Text, nullable=False)
    score = Column(Integer, default=0)  # 0-100
    
    # Análise IA
    eh_correto = Column(Boolean, nullable=True)
    explicacao = Column(Text, nullable=True)
    dicas = Column(Text, nullable=True)
    topicos_relacionados = Column(Text, nullable=True)  # JSON
    
    # Timestamps
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    lancamento = relationship("Lancamento", back_populates="feedback")

    class Config:
        from_attributes = True
