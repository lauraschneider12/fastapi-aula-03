from abc import ABC, abstractmethod
from datetime import datetime

from app.domain.entities.treino import Treino


class TreinoRepository(ABC):

    @abstractmethod
    async def create_treino(
        self,
        data: datetime,
        local: str,
        descricao: str,
        elenco_id: int,
    ) -> Treino:
        ...

    @abstractmethod
    async def list_treinos(self) -> list[Treino]:
        ...

    @abstractmethod
    async def list_treinos_by_elenco(
        self,
        elenco_id: int,
    ) -> list[Treino]:
        ...

    @abstractmethod
    async def get_treino(
        self,
        treino_id: int,
    ) -> Treino | None:
        ...

    @abstractmethod
    async def update_treino(
        self,
        treino_id: int,
        data: datetime,
        local: str,
        descricao: str,
        elenco_id: int,
    ) -> Treino | None:
        ...

    @abstractmethod
    async def delete_treino(
        self,
        treino_id: int,
    ) -> bool:
        ...