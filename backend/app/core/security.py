"""
Funções de segurança: hashing de senha e JWT (JSON Web Tokens).

Conceitos para quem está aprendendo:
  - bcrypt: algoritmo de hashing unidirecional — impossível reverter o hash.
  - JWT: token assinado que prova identidade sem consultar o banco a cada request.
  - O payload do token contém o email do usuário (campo "sub" = subject).
"""
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# ── Configuração de hashing de senha ──────────────────────────────────────────
# CryptContext gerencia automaticamente upgrades de algoritmo no futuro.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha em texto plano corresponde ao hash armazenado no banco.

    Exemplo:
        verify_password("minha_senha", "$2b$12$...hash...")  → True ou False
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Gera o hash bcrypt de uma senha em texto plano.

    NUNCA armazene senhas em texto plano — sempre use esta função.

    Exemplo:
        get_password_hash("minha_senha")  → "$2b$12$...hash..."
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria um JWT token de acesso assinado.

    Parâmetros:
        data         – payload do token; geralmente {"sub": user_email}
        expires_delta – tempo extra de expiração (usa o padrão se None)

    Retorna:
        String JWT no formato "header.payload.signature"

    Exemplo:
        token = create_access_token({"sub": "user@email.com"})
    """
    to_encode = data.copy()

    # Define a expiração do token
    expire = datetime.utcnow() + (
        expires_delta
        if expires_delta
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})

    # Assina o token com a chave secreta
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> Optional[str]:
    """
    Decodifica e valida um JWT token.

    Retorna o email do usuário (campo "sub") se o token for válido,
    ou None se o token estiver expirado/inválido.

    Exemplo:
        email = decode_access_token("eyJ...")  → "user@email.com" ou None
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        return email if email else None
    except JWTError:
        return None
