
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.entities.atleta import Atleta
from app.domain.entities.user import UserIdentity, UserRole
from app.domain.repositories.atleta_repository import AtletaRepository
from app.infrastructure.database.models import AtletaModel


class AtletaRepositoryImpl(AtletaRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, model: AtletaModel) -> Atleta:
        user_identity = None

        if model.user is not None:
            role = getattr(model.user.role, "value", model.user.role)

            user_identity = UserIdentity(
                id=model.user.id,
                email=model.user.email,
                role=UserRole(role),
            )

        return Atleta(
            id=model.id,
            nome=model.nome,
            posicao=model.posicao,
            numero=model.numero,
            status=model.status,
            user_identity=user_identity,
        )

    async def create_atleta(
        self,
        nome: str,
        posicao: str,
        numero: int,
        user_id: UUID,
    ) -> Atleta:
        atleta = AtletaModel(
            nome=nome,
            posicao=posicao,
            numero=numero,
            status=True,
            user_id=user_id,
        )

        self.session.add(atleta)
        await self.session.commit()

        result = await self.session.execute(
            select(AtletaModel)
            .options(selectinload(AtletaModel.user))
            .where(AtletaModel.id == atleta.id)
        )
        atleta = result.scalar_one()

        return self._to_entity(atleta)

    async def list_atletas(self) -> list[Atleta]:
        result = await self.session.execute(
            select(AtletaModel)
            .options(selectinload(AtletaModel.user))
            .order_by(AtletaModel.id)
        )

        return [
            self._to_entity(atleta)
            for atleta in result.scalars().all()
        ]

    async def get_atleta(self, atleta_id: int) -> Atleta | None:
        result = await self.session.execute(
            select(AtletaModel)
            .options(selectinload(AtletaModel.user))
            .where(AtletaModel.id == atleta_id)
        )
        atleta = result.scalar_one_or_none()

        return self._to_entity(atleta) if atleta else None

    async def update_atleta(
        self,
        atleta_id: int,
        nome: str,
        posicao: str,
        numero: int,
    ) -> Atleta | None:
        result = await self.session.execute(
            select(AtletaModel).where(
                AtletaModel.id == atleta_id
            )
        )
        atleta = result.scalar_one_or_none()

        if atleta is None:
            return None

        atleta.nome = nome
        atleta.posicao = posicao
        atleta.numero = numero

        await self.session.commit()

        return await self.get_atleta(atleta_id)

    async def delete_atleta(self, atleta_id: int) -> bool:
        result = await self.session.execute(
            select(AtletaModel).where(
                AtletaModel.id == atleta_id
            )
        )
        atleta = result.scalar_one_or_none()

        if atleta is None:
            return False

        await self.session.delete(atleta)
        await self.session.commit()

        return True
