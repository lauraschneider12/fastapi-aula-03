from abc import ABC, abstractmethod

from app.domain.entities.presenca import Presenca


class PresencaRepository(ABC):

    @abstractmethod
    async def get_by_atleta_and_treino(
        self,
        atleta_id: int,
        treino_id: int
    ) -> Presenca | None:
        pass

    @abstractmethod
    async def create_presenca(
        self,
        atleta_id: int,
        treino_id: int,
        confirmacao: bool | None = None,
        presente: bool | None = None
    ) -> Presenca:
        pass

    @abstractmethod
    async def update_confirmacao(
        self,
        presenca_id: int,
        confirmacao: bool
    ) -> Presenca | None:
        pass

    @abstractmethod
    async def update_presente(
        self,
        presenca_id: int,
        presente: bool
    ) -> Presenca | None:
        pass

    @abstractmethod
    async def list_by_atleta(
        self,
        atleta_id: int
    ) -> list[Presenca]:
        pass

    @abstractmethod
    async def list_by_treino(
        self,
        treino_id: int
    ) -> list[Presenca]:
        pass