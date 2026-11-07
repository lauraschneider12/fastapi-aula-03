from uuid import UUID

from sqlalchemy import select

from app.application.dtos.presenca import AtualizarConfirmacaoDTO, AtualizarPresenteDTO
from app.application.dtos.presenca import (
    AtualizarConfirmacaoDTO,
    AtualizarPresenteDTO,
)

from app.domain.repositories.presenca_repository import PresencaRepository
from app.domain.repositories.treino_repository import TreinoRepository
from app.domain.repositories.atleta_repository import AtletaRepository

from app.infrastructure.database.models.atleta_elenco import AtletaElencoModel


class PresencaUseCases:

    def __init__(
        self,
        presenca_repository: PresencaRepository,
        treino_repository: TreinoRepository,
        atleta_repository: AtletaRepository,
    ):
        self.presenca_repository = presenca_repository
        self.treino_repository = treino_repository
        self.atleta_repository = atleta_repository
        self.session = presenca_repository.session

    async def _validar_vinculo(
        self,
        atleta_id: int,
        elenco_id: int,
    ):
        result = await self.session.execute(
            select(AtletaElencoModel).where(
                AtletaElencoModel.atleta_id == atleta_id,
                AtletaElencoModel.elenco_id == elenco_id,
            )
        )

        vinculo = result.scalar_one_or_none()

        if vinculo is None:
            raise ValueError(
                "A atleta não pertence ao elenco deste treino."
            )

    async def confirmar_presenca(
        self,
        user_id: UUID,
        dados: AtualizarConfirmacaoDTO,
    ):
        try:
            atleta = await self.atleta_repository.get_atleta_by_user_id(
                user_id
            )

            if atleta is None or not atleta.status:
                raise ValueError("Atleta não encontrada ou inativa.")

            treino = await self.treino_repository.get_treino(
                dados.treino_id
            )

            if treino is None:
                raise ValueError("Treino não encontrado.")

            await self._validar_vinculo(
                atleta.id,
                treino.elenco_id,
            )

            presenca = await self.presenca_repository.get_by_atleta_and_treino(
                atleta.id,
                treino.id,
            )

            if presenca is None:
                presenca = await self.presenca_repository.create_presenca(
                    atleta_id=atleta.id,
                    treino_id=treino.id,
                    confirmacao=dados.confirmacao,
                )
            else:
                presenca = await self.presenca_repository.update_confirmacao(
                    presenca.id,
                    dados.confirmacao,
                )

            await self.session.commit()
            return presenca

        except Exception:
            await self.session.rollback()
            raise

    async def registrar_presente(
        self,
        dados: AtualizarPresenteDTO,
    ):
        try:
            atleta = await self.atleta_repository.get_atleta(
                dados.atleta_id
            )

            if atleta is None or not atleta.status:
                raise ValueError("Atleta não encontrada ou inativa.")

            treino = await self.treino_repository.get_treino(
                dados.treino_id
            )

            if treino is None:
                raise ValueError("Treino não encontrado.")

            await self._validar_vinculo(
                atleta.id,
                treino.elenco_id,
            )

            presenca = await self.presenca_repository.get_by_atleta_and_treino(
                atleta.id,
                treino.id,
            )

            if presenca is None:
                presenca = await self.presenca_repository.create_presenca(
                    atleta_id=atleta.id,
                    treino_id=treino.id,
                    presente=dados.presente,
                )
            else:
                presenca = await self.presenca_repository.update_presente(
                    presenca.id,
                    dados.presente,
                )

            await self.session.commit()
            return presenca

        except Exception:
            await self.session.rollback()
            raise

    async def listar_por_atleta(self, atleta_id: int):
        return await self.presenca_repository.list_by_atleta(atleta_id)

    async def listar_por_treino(self, treino_id: int):
        treino = await self.treino_repository.get_treino(treino_id)

        if treino is None:
            raise ValueError("Treino não encontrado.")

        return await self.presenca_repository.list_by_treino(treino_id)
    async def listar_minhas(self, user_id: UUID):
        atleta = await self.atleta_repository.get_atleta_by_user_id(user_id)

        if atleta is None or not atleta.status:
            raise ValueError("Atleta não encontrada ou inativa.")

        return await self.presenca_repository.list_by_atleta(atleta.id)