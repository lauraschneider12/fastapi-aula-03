
from abc import ABC, abstractmethod

from app.domain.entities.elenco import Elenco
from app.domain.entities.atleta import Atleta


class ElencoRepository(ABC):

    @abstractmethod
    async def create_elenco(
        self, ano: int, status: bool
    ) -> Elenco:
        ...

    @abstractmethod
    async def list_elencos(self) -> list[Elenco]:
        ...

    @abstractmethod
    async def get_elenco(
        self, elenco_id: int
    ) -> Elenco | None:
        ...

    @abstractmethod
    async def update_elenco(
        self, elenco_id: int, ano: int, status: bool
    ) -> Elenco | None:
        ...

    @abstractmethod
    async def delete_elenco(self, elenco_id: int) -> bool:
        ...

    @abstractmethod
    async def add_atleta_to_elenco(
        self, elenco_id: int, atleta_id: int
    ) -> bool:
        ...

    @abstractmethod
    async def list_atletas_by_elenco(
        self, elenco_id: int
    ) -> list[Atleta]:
        ...

    @abstractmethod
    async def remove_atleta_from_elenco(
        self, elenco_id: int, atleta_id: int
    ) -> bool:
        ...
