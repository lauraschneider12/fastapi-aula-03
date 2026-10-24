
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.domain.entities.user import UserIdentity, UserRole
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database.models import UserModel
from app.infrastructure.security.password_hasher import password_helper


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, model: UserModel) -> UserIdentity:
        role = getattr(model.role, "value", model.role)

        return UserIdentity(
            id=model.id,
            email=model.email,
            role=UserRole(role),
        )

    async def create_user(
        self,
        email: str,
        senha: str,
        role: str,
    ) -> UserIdentity:
        user = UserModel(
            email=email,
            hashed_password=password_helper.hash(senha),
            is_active=True,
            is_superuser=False,
            is_verified=False,
            role=UserRole(role),
        )

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return self._to_entity(user)

    async def get_user_by_id(
        self,
        user_id: UUID,
    ) -> UserIdentity | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user = result.scalar_one_or_none()

        return self._to_entity(user) if user else None

    async def get_user_by_email(
        self,
        email: str,
    ) -> UserIdentity | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        user = result.scalar_one_or_none()

        return self._to_entity(user) if user else None

    async def update_user(
        self,
        user_id: UUID,
        email: str,
        role: str,
    ) -> UserIdentity | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user = result.scalar_one_or_none()

        if user is None:
            return None

        user.email = email
        user.role = UserRole(role)

        await self.session.commit()
        await self.session.refresh(user)

        return self._to_entity(user)

    async def delete_user(self, user_id: UUID) -> bool:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user = result.scalar_one_or_none()

        if user is None:
            return False

        await self.session.delete(user)
        await self.session.commit()

        return True
