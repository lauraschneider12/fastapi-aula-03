
from fastapi import APIRouter, Depends

from app.infrastructure.security.auth_backend import auth_backend
from app.infrastructure.security.user_manager import (
    fastapi_users,
    current_active_user,
)
from app.infrastructure.database.models import UserModel

router = APIRouter()

# Login e autenticação
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

# Dados do usuário autenticado
@router.get("/auth/me", tags=["Auth"])
async def usuario_logado(
    usuario: UserModel = Depends(current_active_user),
):
    role = getattr(usuario.role, "value", usuario.role)

    return {
        "id": str(usuario.id),
        "email": usuario.email,
        "role": role,
    }
