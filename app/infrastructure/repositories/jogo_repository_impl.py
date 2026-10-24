
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.entities.elenco import ElencoResumo
from app.domain.entities.jogo import Jogo
from app.domain.repositories.jogo_repository import JogoRepository
from app.infrastructure.database.models import JogoModel


class JogoRepositoryImpl(JogoRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def _to_entity(model: JogoModel) -> Jogo:
        return Jogo(
            id=model.id,
            local=model.local,
            time_adversario=model.time_adversario,
            data=model.data,
            ano_elenco=ElencoResumo(ano=model.elenco.ano),
            placar=model.placar,
        )

    async def create_jogo(
        self,
        local: str,
        time_adversario: str,
        data: datetime,
        elenco_id: int,
        placar: str | None = None,
    ) -> Jogo:
        model = JogoModel(
            local=local,
            time_adversario=time_adversario,
            data=data,
            elenco_id=elenco_id,
            placar=placar,
        )
        self.session.add(model)
        await self.session.commit()

        result = await self.session.execute(
            select(JogoModel)
            .options(selectinload(JogoModel.elenco))
            .where(JogoModel.id == model.id)
        )
        model = result.scalar_one()
        return self._to_entity(model)

    async def list_jogos(self) -> list[Jogo]:
        result = await self.session.execute(
            select(JogoModel)
            .options(selectinload(JogoModel.elenco))
            .order_by(JogoModel.data)
        )
        return [self._to_entity(item) for item in result.scalars().all()]

    async def get_jogo(self, jogo_id: int) -> Jogo | None:
        result = await self.session.execute(
            select(JogoModel)
            .options(selectinload(JogoModel.elenco))
            .where(JogoModel.id == jogo_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def update_jogo(
        self,
        jogo_id: int,
        local: str,
        time_adversario: str,
        data: datetime,
        elenco_id: int,
        placar: str | None = None,
    ) -> Jogo | None:
        result = await self.session.execute(
            select(JogoModel).where(JogoModel.id == jogo_id)
        )
        model = result.scalar_one_or_none()

        if model is None:
            return None

        model.local = local
        model.time_adversario = time_adversario
        model.data = data
        model.elenco_id = elenco_id
        model.placar = placar

        await self.session.commit()

        result = await self.session.execute(
            select(JogoModel)
            .options(selectinload(JogoModel.elenco))
            .where(JogoModel.id == jogo_id)
        )
        model = result.scalar_one()
        return self._to_entity(model)

    async def delete_jogo(self, jogo_id: int) -> bool:
        result = await self.session.execute(
            select(JogoModel).where(JogoModel.id == jogo_id)
        )
        model = result.scalar_one_or_none()

        if model is None:
            return False

        await self.session.delete(model)
        await self.session.commit()
        return True
