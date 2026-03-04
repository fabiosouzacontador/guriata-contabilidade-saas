"""
Dependências reutilizáveis do FastAPI (Dependency Injection).

O FastAPI injeta essas funções automaticamente nos endpoints via `Depends()`.

Exemplo de uso em um endpoint protegido:

    @router.get("/perfil")
    async def meu_perfil(current_user: User = Depends(get_current_user)):
        return current_user

Como funciona o fluxo de autenticação:
  1. Cliente envia  Authorization: Bearer <token>  no header
  2. get_current_user extrai e valida o token
  3. Busca o usuário no banco pelo email contido no token
  4. Retorna o objeto User — ou lança 401 se inválido
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database import get_db

# Indica ao FastAPI qual URL emite tokens (aparece no Swagger UI)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    Dependência que extrai e valida o usuário a partir do JWT.

    Levanta HTTPException 401 se o token for inválido ou o usuário
    não existir / estiver inativo.

    Retorna o objeto User do banco de dados.
    """
    # Importação local para evitar import circular (models → database → models)
    from app.models.user import User

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou token expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Decodifica o token e obtém o email
    email = decode_access_token(token)
    if email is None:
        raise credentials_exception

    # Busca o usuário no banco
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    # Usuário inativo não deve conseguir acessar a API
    if not user.ativo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Conta de usuário inativa.",
        )

    return user


def get_current_active_admin(
    current_user=Depends(get_current_user),
):
    """
    Dependência que garante que o usuário logado é um administrador.

    Use em endpoints que só admins podem acessar:

        @router.delete("/users/{id}")
        async def delete_user(admin = Depends(get_current_active_admin)):
            ...
    """
    if not current_user.eh_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores.",
        )
    return current_user
