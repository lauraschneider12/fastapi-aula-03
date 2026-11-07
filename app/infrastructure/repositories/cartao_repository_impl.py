
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.cartao import Cartao, TipoCartao
from app.domain.repositories.cartao_repository import CartaoRepository
from app.infrastructure.database.models import CartaoModel


class CartaoRepositoryImpl(CartaoRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def _to_entity(model: CartaoModel) -> Cartao:
        return Cartao(
            id_cartao=model.id_cartao,
            tipo=TipoCartao(model.tipo),
            id_jogo=model.id_jogo,
            id_jogador=model.id_jogador,
        )

    async def create_cartao(
        self,
        tipo: TipoCartao,
        id_jogo: int,
        id_jogador: int,
    ) -> Cartao:

        cartao_model = CartaoModel(
            tipo=tipo.value,
            id_jogo=id_jogo,
            id_jogador=id_jogador,
        )

        self.session.add(cartao_model)
        await self.session.flush()
        await self.session.refresh(cartao_model)

        return self._to_entity(cartao_model)

    async def list_cartoes(self) -> list[Cartao]:

        result = await self.session.execute(
            select(CartaoModel)
        )

        return [
            self._to_entity(item)
            for item in result.scalars().all()
        ]

    async def get_cartao(
        self,
        id_cartao: int,
    ) -> Cartao | None:

        result = await self.session.execute(
            select(CartaoModel).where(
                CartaoModel.id_cartao == id_cartao
            )
        )

        cartao = result.scalar_one_or_none()

        if cartao is None:
            return None

        return self._to_entity(cartao)

    async def update_cartao(
        self,
        id_cartao: int,
        tipo: TipoCartao,
        id_jogo: int,
        id_jogador: int,
    ) -> Cartao | None:

        result = await self.session.execute(
            select(CartaoModel).where(
                CartaoModel.id_cartao == id_cartao
            )
        )

        cartao_model = result.scalar_one_or_none()

        if cartao_model is None:
            return None

        cartao_model.tipo = tipo.value
        cartao_model.id_jogo = id_jogo
        cartao_model.id_jogador = id_jogador

        await self.session.flush()
        await self.session.refresh(cartao_model)

        return self._to_entity(cartao_model)

    async def delete_cartao(
        self,
        id_cartao: int,
    ) -> bool:

        result = await self.session.execute(
            select(CartaoModel).where(
                CartaoModel.id_cartao == id_cartao
            )
        )

        cartao_model = result.scalar_one_or_none()

        if cartao_model is None:
            return False

        await self.session.delete(cartao_model)
        await self.session.flush()

        return True
