
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.gol import Gol
from app.domain.repositories.gol_repository import GolRepository
from app.infrastructure.database.models import GolModel


class GolRepositoryImpl(GolRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def _to_entity(model: GolModel) -> Gol:
        return Gol(
            id_gol=model.id_gol,
            id_jogo=model.id_jogo,
            id_jogador=model.id_jogador,
        )

    async def create_gol(
        self,
        id_jogo: int,
        id_jogador: int,
    ) -> Gol:

        gol_model = GolModel(
            id_jogo=id_jogo,
            id_jogador=id_jogador,
        )

        self.session.add(gol_model)
        await self.session.flush()
        await self.session.refresh(gol_model)

        return self._to_entity(gol_model)

    async def list_gols(self) -> list[Gol]:

        result = await self.session.execute(
            select(GolModel)
        )

        return [
            self._to_entity(item)
            for item in result.scalars().all()
        ]

    async def list_gols_for_time_local(
        self,
        id_jogo: int,
    ) -> list[Gol]:

        result = await self.session.execute(
            select(GolModel).where(
                GolModel.id_jogo == id_jogo,
                GolModel.id_jogador != 100,
            )
        )

        return [
            self._to_entity(item)
            for item in result.scalars().all()
        ]

    async def list_gols_for_time_visitante(
        self,
        id_jogo: int,
    ) -> list[Gol]:

        result = await self.session.execute(
            select(GolModel).where(
                GolModel.id_jogo == id_jogo,
                GolModel.id_jogador == 100,
            )
        )

        return [
            self._to_entity(item)
            for item in result.scalars().all()
        ]

    async def get_gol(
        self,
        id_gol: int,
    ) -> Gol | None:

        result = await self.session.execute(
            select(GolModel).where(
                GolModel.id_gol == id_gol
            )
        )

        gol_model = result.scalar_one_or_none()

        if gol_model is None:
            return None

        return self._to_entity(gol_model)

    async def update_gol(
        self,
        id_gol: int,
        id_jogo: int,
        id_jogador: int,
    ) -> Gol | None:

        result = await self.session.execute(
            select(GolModel).where(
                GolModel.id_gol == id_gol
            )
        )

        gol_model = result.scalar_one_or_none()

        if gol_model is None:
            return None

        gol_model.id_jogo = id_jogo
        gol_model.id_jogador = id_jogador

        await self.session.flush()
        await self.session.refresh(gol_model)

        return self._to_entity(gol_model)

    async def delete_gol(
        self,
        id_gol: int,
    ) -> bool:

        result = await self.session.execute(
            select(GolModel).where(
                GolModel.id_gol == id_gol
            )
        )

        gol_model = result.scalar_one_or_none()

        if gol_model is None:
            return False

        await self.session.delete(gol_model)
        await self.session.flush()

        return True
