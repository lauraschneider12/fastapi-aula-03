
from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.user import UserIdentity


class UserRepository(ABC):

    @abstractmethod
    async def create_user(
        self,
        email: str,
        senha: str,
        role: str,
    ) -> UserIdentity:
        ...

    @abstractmethod
    async def get_user_by_id(
        self,
        user_id: UUID,
    ) -> UserIdentity | None:
        ...

    @abstractmethod
    async def get_user_by_email(
        self,
        email: str,
    ) -> UserIdentity | None:
        ...

    @abstractmethod
    async def update_user(
        self,
        user_id: UUID,
        email: str,
        role: str,
    ) -> UserIdentity | None:
        ...

    @abstractmethod
    async def delete_user(
        self,
        user_id: UUID,
    ) -> bool:
        ...
