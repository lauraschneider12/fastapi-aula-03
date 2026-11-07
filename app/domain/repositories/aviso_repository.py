from abc import ABC, abstractmethod
from app.domain.entities.aviso import Aviso


class AvisoRepository(ABC):

    @abstractmethod
    async def create_aviso(
        self,
        titulo: str,
        conteudo: str,
        elenco_id: int | None,
        administrador_id: int,
    ) -> Aviso:
        ...

    @abstractmethod
    async def list_avisos(self) -> list[Aviso]:
        ...

    @abstractmethod
    async def list_avisos_by_elenco(
        self,
        elenco_id: int,
    ) -> list[Aviso]:
        ...

    @abstractmethod
    async def get_aviso(self, aviso_id: int) -> Aviso | None:
        ...

    @abstractmethod
    async def update_aviso(
        self,
        aviso_id: int,
        titulo: str,
        conteudo: str,
        elenco_id: int | None,
    ) -> Aviso | None:
        ...

    @abstractmethod
    async def delete_aviso(self, aviso_id: int) -> bool:
        ...