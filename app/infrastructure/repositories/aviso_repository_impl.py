from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.aviso import Aviso
from app.domain.repositories.aviso_repository import AvisoRepository
from app.infrastructure.database.models.aviso import AvisoModel


class AvisoRepositoryImpl(AvisoRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, model: AvisoModel) -> Aviso:
        return Aviso(
            id=model.id,
            titulo=model.titulo,
            conteudo=model.conteudo,
            data_publicacao=model.data_publicacao,
            elenco_id=model.elenco_id,
            administrador_id=model.administrador_id,
        )

    async def create_aviso(
        self,
        titulo: str,
        conteudo: str,
        elenco_id: int | None,
        administrador_id: int,
    ) -> Aviso:

        model = AvisoModel(
            titulo=titulo,
            conteudo=conteudo,
            elenco_id=elenco_id,
            administrador_id=administrador_id,
        )

        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)

        return self._to_entity(model)

    async def list_avisos(self) -> list[Aviso]:
        result = await self.session.execute(
            select(AvisoModel).order_by(
                AvisoModel.data_publicacao.desc()
            )
        )

        return [
            self._to_entity(model)
            for model in result.scalars().all()
        ]

    async def list_avisos_by_elenco(
        self,
        elenco_id: int,
    ) -> list[Aviso]:

        result = await self.session.execute(
            select(AvisoModel).where(
                (AvisoModel.elenco_id == elenco_id)
                | (AvisoModel.elenco_id.is_(None))
            ).order_by(AvisoModel.data_publicacao.desc())
        )

        return [
            self._to_entity(model)
            for model in result.scalars().all()
        ]

    async def get_aviso(self, aviso_id: int) -> Aviso | None:
        model = await self.session.get(AvisoModel, aviso_id)

        return self._to_entity(model) if model else None

    async def update_aviso(
        self,
        aviso_id: int,
        titulo: str,
        conteudo: str,
        elenco_id: int | None,
    ) -> Aviso | None:

        model = await self.session.get(AvisoModel, aviso_id)

        if model is None:
            return None

        model.titulo = titulo
        model.conteudo = conteudo
        model.elenco_id = elenco_id

        await self.session.flush()
        await self.session.refresh(model)

        return self._to_entity(model)

    async def delete_aviso(self, aviso_id: int) -> bool:
        model = await self.session.get(AvisoModel, aviso_id)

        if model is None:
            return False

        await self.session.delete(model)
        await self.session.flush()

        return True