
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import UserIdentity, UserRole
from app.domain.entities.elenco import Elenco
from app.domain.entities.atleta import Atleta
from app.domain.repositories.elenco_repository import ElencoRepository
from app.infrastructure.database.models import (
    ElencoModel,
    AtletaModel,
    AtletaElencoModel,
)


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

    async def create_elenco(
        self, ano: int, status: bool
    ) -> Elenco:
        model = ElencoModel(ano=ano, status=status)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def list_elencos(self) -> list[Elenco]:
        result = await self.session.execute(
            select(ElencoModel).order_by(ElencoModel.ano.desc())
        )
        return [
            self._to_entity(item)
            for item in result.scalars().all()
        ]

    async def get_elenco(
        self, elenco_id: int
    ) -> Elenco | None:
        result = await self.session.execute(
            select(ElencoModel).where(
                ElencoModel.id == elenco_id
            )
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def update_elenco(
        self, elenco_id: int, ano: int, status: bool
    ) -> Elenco | None:
        result = await self.session.execute(
            select(ElencoModel).where(
                ElencoModel.id == elenco_id
            )
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
            select(ElencoModel).where(
                ElencoModel.id == elenco_id
            )
        )
        model = result.scalar_one_or_none()

        if model is None:
            return False

        # Não permite excluir um elenco que possua jogos associados.
        if model.jogos:
            raise ValueError(
                "Não é possível excluir um elenco que possui jogos associados."
            )

        try:
            await self.session.delete(model)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        return True

    async def add_atleta_to_elenco(
        self, elenco_id: int, atleta_id: int
    ) -> bool:
        # Verifica se o elenco existe.
        elenco_model = await self.session.get(
            ElencoModel, elenco_id
        )
        if elenco_model is None:
            return False

        # Verifica se o atleta existe.
        atleta_model = await self.session.get(
            AtletaModel, atleta_id
        )
        if atleta_model is None:
            return False

        # Verifica se a associação já existe.
        associacao = await self.session.get(
            AtletaElencoModel,
            {
                "atleta_id": atleta_id,
                "elenco_id": elenco_id,
            },
        )
        if associacao is not None:
            return False

        # Cria somente a associação.
        associacao = AtletaElencoModel(
            atleta_id=atleta_id,
            elenco_id=elenco_id,
        )

        try:
            self.session.add(associacao)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        return True

    @staticmethod
    def _atleta_to_entity(model: AtletaModel) -> Atleta:
        user_identity = None

        if model.user is not None:
            role = getattr(
                model.user.role,
                "value",
                model.user.role,
            )

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

    async def list_atletas_by_elenco(
        self, elenco_id: int
    ) -> list[Atleta]:
        result = await self.session.execute(
            select(AtletaModel)
            .join(
                AtletaElencoModel,
                AtletaElencoModel.atleta_id == AtletaModel.id,
            )
            .where(
                AtletaElencoModel.elenco_id == elenco_id
            )
            .options(selectinload(AtletaModel.user))
            .order_by(AtletaModel.id)
        )

        atletas = result.scalars().all()

        return [
            self._atleta_to_entity(atleta)
            for atleta in atletas
        ]

    async def remove_atleta_from_elenco(
        self, elenco_id: int, atleta_id: int
    ) -> bool:
        associacao = await self.session.get(
            AtletaElencoModel,
            {
                "atleta_id": atleta_id,
                "elenco_id": elenco_id,
            },
        )

        if associacao is None:
            return False

        try:
            await self.session.delete(associacao)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        return True
