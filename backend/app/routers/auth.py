"""
Router de autenticação JWT.

Endpoints disponíveis:
  POST /api/auth/register  – cria um novo usuário
  POST /api/auth/login     – autentica e retorna o JWT
  GET  /api/auth/me        – retorna o perfil do usuário logado (rota protegida)

Fluxo de aprendizado:
  1. Chame /register para criar sua conta.
  2. Chame /login para receber o access_token.
  3. Use o token no header:  Authorization: Bearer <token>
  4. Chame /me para ver seu perfil — sem o token retorna 401.
"""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, get_password_hash, verify_password
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserResponse

router = APIRouter()


# ── POST /register ────────────────────────────────────────────────────────────


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar novo usuário",
    description="Cria uma nova conta de usuário. O email deve ser único.",
)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Registra um novo usuário no sistema.

    - **email**: deve ser único — retorna 400 se já existir
    - **nome**: nome completo do usuário
    - **senha**: será hasheada com bcrypt antes de salvar
    - **eh_professor**: define permissão de professor (padrão: false)
    """
    # Verifica se o email já está cadastrado
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado. Tente fazer login.",
        )

    # Cria o usuário com a senha hasheada (NUNCA salvar texto plano!)
    db_user = User(
        email=user_in.email,
        nome=user_in.nome,
        senha_hash=get_password_hash(user_in.senha),
        eh_professor=user_in.eh_professor,
        eh_admin=user_in.eh_admin,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ── POST /login ───────────────────────────────────────────────────────────────


@router.post(
    "/login",
    response_model=Token,
    summary="Login — obtém token JWT",
    description=(
        "Autentica com email e senha. "
        "Retorna um access_token JWT para usar nas rotas protegidas."
    ),
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Autentica o usuário e devolve um JWT.

    O Swagger UI usa o campo `username` do OAuth2PasswordRequestForm
    — informe o **email** nesse campo ao testar pelo /docs.

    Retorno:
        { "access_token": "eyJ...", "token_type": "bearer" }
    """
    # Busca o usuário pelo email (username no formulário OAuth2)
    user = db.query(User).filter(User.email == form_data.username).first()

    # Verifica existência e senha — NUNCA informe qual dos dois está errado!
    if not user or not verify_password(form_data.password, user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.ativo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Conta inativa. Entre em contato com o suporte.",
        )

    # Gera o token com expiração configurável
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


# ── GET /me ───────────────────────────────────────────────────────────────────


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Meu perfil (rota protegida)",
    description="Retorna os dados do usuário autenticado. Requer token JWT válido.",
)
def me(current_user: User = Depends(get_current_user)):
    """
    Retorna o perfil do usuário atualmente logado.

    Esta é uma **rota protegida** — envie o header:
        Authorization: Bearer <access_token>

    No Swagger UI clique no cadeado 🔒 e cole o token para testar.
    """
    return current_user
