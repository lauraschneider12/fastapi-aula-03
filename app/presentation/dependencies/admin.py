from fastapi import Depends, HTTPException, status

from app.domain.entities.user import UserRole
from app.infrastructure.database.models import UserModel
from app.infrastructure.security.user_manager import current_active_user


async def require_admin(
    user: UserModel = Depends(current_active_user),
) -> UserModel:
    role = getattr(user.role, "value", user.role)

    if role != UserRole.ADMINISTRADOR.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem realizar esta operação.",
        )

    return user