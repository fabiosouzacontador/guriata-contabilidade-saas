"""
Schemas Pydantic para autenticação e usuário.

Pydantic valida e serializa dados automaticamente:
  - Entrada  (request body)  → UserCreate, UserLogin
  - Saída    (response body) → UserResponse, Token
  - Interno  (token payload) → TokenData

Diferença importante:
  UserCreate  – inclui a senha em texto plano (nunca armazenar assim no banco!)
  UserResponse – nunca expõe a senha; usa `from_attributes=True` para ler do ORM.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# ── Token ─────────────────────────────────────────────────────────────────────


class Token(BaseModel):
    """Resposta do endpoint /login — retorna o JWT ao cliente."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """
    Payload interno extraído do JWT após validação.
    Usado em dependencies.py para identificar o usuário logado.
    """

    email: Optional[str] = None


# ── Usuário ───────────────────────────────────────────────────────────────────


class UserBase(BaseModel):
    """Campos compartilhados entre schemas de usuário."""

    email: EmailStr
    nome: str
    eh_professor: bool = False
    eh_admin: bool = False


class UserCreate(UserBase):
    """
    Schema de criação de usuário (registro).
    Inclui a senha em texto plano — será hasheada antes de salvar no banco.
    """

    senha: str


class UserLogin(BaseModel):
    """Schema de login — email + senha em texto plano."""

    email: EmailStr
    senha: str


class UserUpdate(BaseModel):
    """Schema de atualização parcial de usuário (campos opcionais)."""

    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    eh_professor: Optional[bool] = None


class UserResponse(UserBase):
    """
    Schema de resposta — exposto ao cliente.
    NUNCA inclui a senha ou o hash da senha.
    """

    id: int
    ativo: bool
    company_id: Optional[int] = None
    criado_em: datetime
    atualizado_em: Optional[datetime] = None

    class Config:
        # Permite criar o schema a partir de um objeto ORM (SQLAlchemy model)
        from_attributes = True


# ── Empresa ───────────────────────────────────────────────────────────────────


class CompanyBase(BaseModel):
    """Campos compartilhados entre schemas de empresa."""

    name: str
    cnpj: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class CompanyCreate(CompanyBase):
    """Schema de criação de empresa."""

    pass


class CompanyResponse(CompanyBase):
    """Schema de resposta de empresa."""

    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
