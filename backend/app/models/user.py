"""
Modelos SQLAlchemy: Usuário e Empresa.

Esses são os modelos centrais do SaaS:
  - Company: representa uma empresa cliente do sistema (multi-tenant).
  - User:    representa um usuário autenticado, opcionalmente ligado a uma empresa.
"""
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Company(Base):
    """
    Empresa cliente do SaaS de contabilidade.

    No modelo multi-tenant cada empresa isola seus próprios dados
    (escolas, turmas, lançamentos etc.).
    """

    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    cnpj = Column(String(18), unique=True, nullable=True, index=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)

    # Timestamps automáticos
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Um-para-muitos: empresa → usuários
    users = relationship("User", back_populates="company")

    class Config:
        from_attributes = True


class User(Base):
    """
    Usuário do sistema.

    Armazena credenciais (email + senha hasheada) e flags de permissão.
    Pode estar associado a uma Company (multi-tenant SaaS).
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    nome = Column(String(255), nullable=False)
    # Armazenar SEMPRE o hash, nunca a senha em texto plano!
    senha_hash = Column(String(255), nullable=False)
    ativo = Column(Boolean, default=True)
    eh_professor = Column(Boolean, default=False)
    eh_admin = Column(Boolean, default=False)

    # FK opcional para empresa (SaaS multi-tenant)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)

    # Timestamps automáticos
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    company = relationship("Company", back_populates="users")
    escolas = relationship("Escola", back_populates="criador")
    turmas = relationship("Turma", back_populates="professor")
    alunos = relationship("Aluno", back_populates="usuario")
    lancamentos = relationship("Lancamento", back_populates="usuario")

    class Config:
        from_attributes = True
