
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.elenco import Elenco
from app.domain.repositories.elenco_repository import ElencoRepository
from app.infrastructure.database.models import ElencoModel


class ElencoRepositoryImpl(ElencoRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def _to_entity(model: ElencoModel) -> Elenco:
        return Elenco(
            id=model.id,
            ano=model.ano,
            status=model.status,
        )

    async def create_elenco(self, ano: int, status: bool) -> Elenco:
        model = ElencoModel(ano=ano, status=status)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def list_elencos(self) -> list[Elenco]:
        result = await self.session.execute(
            select(ElencoModel).order_by(ElencoModel.ano.desc())
        )
        return [self._to_entity(item) for item in result.scalars().all()]

    async def get_elenco(self, elenco_id: int) -> Elenco | None:
        result = await self.session.execute(
            select(ElencoModel).where(ElencoModel.id == elenco_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def update_elenco(
        self, elenco_id: int, ano: int, status: bool
    ) -> Elenco | None:
        result = await self.session.execute(
            select(ElencoModel).where(ElencoModel.id == elenco_id)
        )
        model = result.scalar_one_or_none()

        if model is None:
            return None

        model.ano = ano
        model.status = status
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def delete_elenco(self, elenco_id: int) -> bool:
        result = await self.session.execute(
            select(ElencoModel).where(ElencoModel.id == elenco_id)
        )
        model = result.scalar_one_or_none()

        if model is None:
            return False

        await self.session.delete(model)

        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        return True
