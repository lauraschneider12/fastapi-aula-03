
from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.atleta import Atleta


class AtletaRepository(ABC):

    @abstractmethod
    async def create_atleta(
        self,
        nome: str,
        posicao: str,
        numero: int,
        user_id: UUID,
    ) -> Atleta:
        ...

    @abstractmethod
    async def list_atletas(self) -> list[Atleta]:
        ...

    @abstractmethod
    async def get_atleta(self, atleta_id: int) -> Atleta | None:
        ...

    @abstractmethod
    async def update_atleta(
        self,
        atleta_id: int,
        nome: str,
        posicao: str,
        numero: int,
        status: bool,
    ) -> Atleta | None:
        ...

    @abstractmethod
    async def delete_atleta(self, atleta_id: int) -> bool:
        ...
    @abstractmethod
    async def get_atleta_by_user_id(self, user_id: UUID) -> Atleta | None:
     ...
