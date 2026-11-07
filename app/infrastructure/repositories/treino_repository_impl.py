from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.treino import Treino
from app.domain.repositories.treino_repository import TreinoRepository

from app.infrastructure.database.models import TreinoModel


class TreinoRepositoryImpl(TreinoRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def _to_entity(model: TreinoModel) -> Treino:
        return Treino(
            id=model.id,
            data=model.data,
            local=model.local,
            descricao=model.descricao,
            elenco_id=model.elenco_id,
        )

    async def create_treino(
        self,
        data: datetime,
        local: str,
        descricao: str,
        elenco_id: int,
    ) -> Treino:

        model = TreinoModel(
            data=data,
            local=local,
            descricao=descricao,
            elenco_id=elenco_id,
        )

        self.session.add(model)
        await self.session.flush()

        return self._to_entity(model)

    async def list_treinos(self) -> list[Treino]:

        result = await self.session.execute(
            select(TreinoModel)
            .order_by(TreinoModel.data)
        )

        modelos = result.scalars().all()

        return [
            self._to_entity(item)
            for item in modelos
        ]

    async def list_treinos_by_elenco(
        self,
        elenco_id: int,
    ) -> list[Treino]:

        result = await self.session.execute(
            select(TreinoModel)
            .where(TreinoModel.elenco_id == elenco_id)
            .order_by(TreinoModel.data)
        )

        modelos = result.scalars().all()

        return [
            self._to_entity(item)
            for item in modelos
        ]

    async def get_treino(
        self,
        treino_id: int,
    ) -> Treino | None:

        result = await self.session.execute(
            select(TreinoModel)
            .where(TreinoModel.id == treino_id)
        )

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._to_entity(model)

    async def update_treino(
        self,
        treino_id: int,
        data: datetime,
        local: str,
        descricao: str,
        elenco_id: int,
    ) -> Treino | None:

        result = await self.session.execute(
            select(TreinoModel)
            .where(TreinoModel.id == treino_id)
        )

        model = result.scalar_one_or_none()

        if model is None:
            return None

        model.data = data
        model.local = local
        model.descricao = descricao
        model.elenco_id = elenco_id

        await self.session.flush()

        return self._to_entity(model)

    async def delete_treino(self, treino_id: int) -> bool:

        result = await self.session.execute(
            select(TreinoModel)
            .where(TreinoModel.id == treino_id)
        )

        model = result.scalar_one_or_none()

        if model is None:
            return False

        await self.session.delete(model)
        await self.session.flush()

        return True