
from abc import ABC, abstractmethod

from app.domain.entities.gol import Gol


class GolRepository(ABC):

    @abstractmethod
    async def create_gol(
        self,
        id_jogo: int,
        id_jogador: int,
    ) -> Gol:
        ...

    @abstractmethod
    async def list_gols(self) -> list[Gol]:
        ...

    @abstractmethod
    async def list_gols_for_time_local(
        self,
        id_jogo: int,
    ) -> list[Gol]:
        ...

    @abstractmethod
    async def list_gols_for_time_visitante(
        self,
        id_jogo: int,
    ) -> list[Gol]:
        ...

    @abstractmethod
    async def get_gol(
        self,
        id_gol: int,
    ) -> Gol | None:
        ...

    @abstractmethod
    async def update_gol(
        self,
        id_gol: int,
        id_jogo: int,
        id_jogador: int,
    ) -> Gol | None:
        ...

    @abstractmethod
    async def delete_gol(
        self,
        id_gol: int,
    ) -> bool:
        ...
