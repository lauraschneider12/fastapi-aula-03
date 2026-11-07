
from abc import ABC, abstractmethod

from app.domain.entities.cartao import Cartao, TipoCartao


class CartaoRepository(ABC):

    @abstractmethod
    async def create_cartao(
        self,
        tipo: TipoCartao,
        id_jogo: int,
        id_jogador: int,
    ) -> Cartao:
        ...

    @abstractmethod
    async def list_cartoes(self) -> list[Cartao]:
        ...

    @abstractmethod
    async def get_cartao(
        self,
        id_cartao: int,
    ) -> Cartao | None:
        ...

    @abstractmethod
    async def update_cartao(
        self,
        id_cartao: int,
        tipo: TipoCartao,
        id_jogo: int,
        id_jogador: int,
    ) -> Cartao | None:
        ...

    @abstractmethod
    async def delete_cartao(
        self,
        id_cartao: int,
    ) -> bool:
        ...
