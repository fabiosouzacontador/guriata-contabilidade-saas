"""
Pacote de modelos SQLAlchemy.

Exporta todos os modelos para que o código existente continue funcionando
com o import  `from app import models`.

Estrutura:
  models/user.py  → User, Company  (autenticação e multi-tenant)
  models/__init__ → Escola, Turma, Aluno, Conta, Lancamento, FeedbackIA
                    (domínio contábil-educacional)
"""

# ── Modelos de autenticação e empresa ─────────────────────────────────────────
# Importados do módulo dedicado para facilitar testes e leitura isolada.
from app.models.user import Company, User  # noqa: F401

# ── Dependências dos modelos restantes ────────────────────────────────────────
import enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

# ── Enums de domínio ──────────────────────────────────────────────────────────


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


# ── Escola ────────────────────────────────────────────────────────────────────


class Escola(Base):
    """Modelo de escola / instituição educacional."""

    __tablename__ = "escolas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False, index=True)
    descricao = Column(Text, nullable=True)
    cnpj = Column(String(18), unique=True, nullable=True)
    endereco = Column(String(255), nullable=True)
    telefone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)

    criador_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ativa = Column(Boolean, default=True)

    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())

    criador = relationship("User", back_populates="escolas")
    turmas = relationship("Turma", back_populates="escola", cascade="all, delete-orphan")
    contas = relationship("Conta", back_populates="escola", cascade="all, delete-orphan")

    class Config:
        from_attributes = True


# ── Turma ─────────────────────────────────────────────────────────────────────


class Turma(Base):
    """Modelo de turma / grupo de alunos."""

    __tablename__ = "turmas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=True)
    periodo = Column(String(50), nullable=True)

    escola_id = Column(Integer, ForeignKey("escolas.id"), nullable=False)
    professor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ativa = Column(Boolean, default=True)

    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())

    escola = relationship("Escola", back_populates="turmas")
    professor = relationship("User", back_populates="turmas")
    alunos = relationship("Aluno", back_populates="turma", cascade="all, delete-orphan")
    lancamentos = relationship("Lancamento", back_populates="turma")

    class Config:
        from_attributes = True


# ── Aluno ─────────────────────────────────────────────────────────────────────


class Aluno(Base):
    """Modelo de aluno."""

    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    matricula = Column(String(50), unique=True, nullable=False, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    cpf = Column(String(14), unique=True, nullable=True)

    turma_id = Column(Integer, ForeignKey("turmas.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(Enum(StatusAlunoEnum), default=StatusAlunoEnum.ATIVO)

    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())

    turma = relationship("Turma", back_populates="alunos")
    usuario = relationship("User", back_populates="alunos")

    class Config:
        from_attributes = True


# ── Conta ─────────────────────────────────────────────────────────────────────


class Conta(Base):
    """Modelo de conta contábil (plano de contas)."""

    __tablename__ = "contas"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(20), nullable=False)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=True)
    tipo = Column(Enum(TipoContaEnum), nullable=False)

    saldo_inicial = Column(Float, default=0.0)
    saldo_atual = Column(Float, default=0.0)

    escola_id = Column(Integer, ForeignKey("escolas.id"), nullable=False)
    conta_pai_id = Column(Integer, ForeignKey("contas.id"), nullable=True)
    ativa = Column(Boolean, default=True)

    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())

    escola = relationship("Escola", back_populates="contas")
    # Self-referential adjacency list: remote_side on the MANY-TO-ONE side (conta_pai)
    contas_filhas = relationship(
        "Conta",
        back_populates="conta_pai",
        foreign_keys=[conta_pai_id],
    )
    conta_pai = relationship(
        "Conta",
        back_populates="contas_filhas",
        remote_side=[id],
        foreign_keys=[conta_pai_id],
    )
    lancamentos_debito = relationship(
        "Lancamento",
        foreign_keys="Lancamento.conta_debito_id",
        back_populates="conta_debito",
    )
    lancamentos_credito = relationship(
        "Lancamento",
        foreign_keys="Lancamento.conta_credito_id",
        back_populates="conta_credito",
    )

    class Config:
        from_attributes = True


# ── Lancamento ────────────────────────────────────────────────────────────────


class Lancamento(Base):
    """Modelo de lançamento contábil."""

    __tablename__ = "lancamentos"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String(50), unique=True, nullable=False, index=True)
    descricao = Column(String(255), nullable=False)
    valor = Column(Float, nullable=False)

    conta_debito_id = Column(Integer, ForeignKey("contas.id"), nullable=False)
    conta_credito_id = Column(Integer, ForeignKey("contas.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    turma_id = Column(Integer, ForeignKey("turmas.id"), nullable=True)
    status = Column(Enum(StatusLancamentoEnum), default=StatusLancamentoEnum.PENDENTE)

    data_lancamento = Column(DateTime, nullable=False, default=func.now)
    data_vencimento = Column(DateTime, nullable=True)
    observacoes = Column(Text, nullable=True)

    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())

    conta_debito = relationship(
        "Conta", foreign_keys=[conta_debito_id], back_populates="lancamentos_debito"
    )
    conta_credito = relationship(
        "Conta", foreign_keys=[conta_credito_id], back_populates="lancamentos_credito"
    )
    usuario = relationship("User", back_populates="lancamentos")
    turma = relationship("Turma", back_populates="lancamentos")
    feedback = relationship("FeedbackIA", back_populates="lancamento", cascade="all, delete-orphan")

    class Config:
        from_attributes = True


# ── FeedbackIA ────────────────────────────────────────────────────────────────


class FeedbackIA(Base):
    """Modelo de feedback da IA Tutor."""

    __tablename__ = "feedback_ia"

    id = Column(Integer, primary_key=True, index=True)
    lancamento_id = Column(Integer, ForeignKey("lancamentos.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    tipo_feedback = Column(String(50), nullable=False)
    mensagem = Column(Text, nullable=False)
    score = Column(Integer, default=0)

    eh_correto = Column(Boolean, nullable=True)
    explicacao = Column(Text, nullable=True)
    dicas = Column(Text, nullable=True)
    topicos_relacionados = Column(Text, nullable=True)

    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    lancamento = relationship("Lancamento", back_populates="feedback")

    class Config:
        from_attributes = True
