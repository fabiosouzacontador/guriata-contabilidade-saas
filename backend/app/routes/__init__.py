from .auth import router as auth_router
from .users import router as users_router
from .contas import router as contas_router
from .lancamentos import router as lancamentos_router
from .turmas import router as turmas_router
from .escolas import router as escolas_router
from .atividades import router as atividades_router
from .relatorios import router as relatorios_router
from .ia_tutor import router as ia_tutor_router

__all__ = [
    "auth_router",
    "users_router",
    "contas_router",
    "lancamentos_router",
    "turmas_router",
    "escolas_router",
    "atividades_router",
    "relatorios_router",
    "ia_tutor_router",
]