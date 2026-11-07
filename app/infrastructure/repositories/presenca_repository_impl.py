from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.presenca import Presenca
from app.domain.repositories.presenca_repository import PresencaRepository
from app.infrastructure.database.models.presenca import PresencaModel


class PresencaRepositoryImpl(PresencaRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, model: PresencaModel) -> Presenca:
        return Presenca(
            id=model.id,
            atleta_id=model.atleta_id,
            treino_id=model.treino_id,
            confirmacao=model.confirmacao,
            presente=model.presente,
            confirmado_em=model.confirmado_em,
            registrado_em=model.registrado_em,
        )

    async def get_by_atleta_and_treino(
        self,
        atleta_id: int,
        treino_id: int,
    ) -> Presenca | None:

        result = await self.session.execute(
            select(PresencaModel).where(
                PresencaModel.atleta_id == atleta_id,
                PresencaModel.treino_id == treino_id,
            )
        )

        model = result.scalar_one_or_none()

        return self._to_entity(model) if model else None

    async def create_presenca(
        self,
        atleta_id: int,
        treino_id: int,
        confirmacao: bool | None = None,
        presente: bool | None = None,
    ) -> Presenca:

        agora = datetime.now(timezone.utc)

        model = PresencaModel(
            atleta_id=atleta_id,
            treino_id=treino_id,
            confirmacao=confirmacao,
            presente=presente,
            confirmado_em=agora if confirmacao is not None else None,
            registrado_em=agora if presente is not None else None,
        )

        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)

        return self._to_entity(model)

    async def update_confirmacao(
        self,
        presenca_id: int,
        confirmacao: bool,
    ) -> Presenca | None:

        model = await self.session.get(PresencaModel, presenca_id)

        if model is None:
            return None

        model.confirmacao = confirmacao
        model.confirmado_em = datetime.now(timezone.utc)

        await self.session.flush()
        await self.session.refresh(model)

        return self._to_entity(model)

    async def update_presente(
        self,
        presenca_id: int,
        presente: bool,
    ) -> Presenca | None:

        model = await self.session.get(PresencaModel, presenca_id)

        if model is None:
            return None

        model.presente = presente
        model.registrado_em = datetime.now(timezone.utc)

        await self.session.flush()
        await self.session.refresh(model)

        return self._to_entity(model)

    async def list_by_atleta(
        self,
        atleta_id: int,
    ) -> list[Presenca]:

        result = await self.session.execute(
            select(PresencaModel).where(
                PresencaModel.atleta_id == atleta_id
            )
        )

        return [
            self._to_entity(model)
            for model in result.scalars().all()
        ]

    async def list_by_treino(
        self,
        treino_id: int,
    ) -> list[Presenca]:

        result = await self.session.execute(
            select(PresencaModel).where(
                PresencaModel.treino_id == treino_id
            )
        )

        return [
            self._to_entity(model)
            for model in result.scalars().all()
        ]