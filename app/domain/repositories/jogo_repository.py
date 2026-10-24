from abc import ABC, abstractmethod
from datetime import datetime

from app.domain.entities.jogo import Jogo


class JogoRepository(ABC):

    @abstractmethod
    async def create_jogo(
        self,
        local: str,
        time_adversario: str,
        data: datetime,
        elenco_id: int,
        placar: str | None = None,
    ) -> Jogo:
        ...

    @abstractmethod
    async def list_jogos(self) -> list[Jogo]:
        ...

    @abstractmethod
    async def get_jogo(
        self, jogo_id: int
    ) -> Jogo | None:
        ...

    @abstractmethod
    async def update_jogo(
        self,
        jogo_id: int,
        local: str,
        time_adversario: str,
        data: datetime,
        elenco_id: int,
        placar: str | None = None,
    ) -> Jogo | None:
        ...

    @abstractmethod
    async def delete_jogo(self, jogo_id: int) -> bool:
        ...