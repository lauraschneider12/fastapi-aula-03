from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dtos.aviso import (
    CriarAvisoDTO,
    AtualizarAvisoDTO,
)
from app.domain.repositories.aviso_repository import AvisoRepository
from app.infrastructure.database.models.administrador import AdministradorModel
from app.infrastructure.database.models.elenco import ElencoModel


class AvisoUseCases:

    def __init__(
        self,
        aviso_repository: AvisoRepository,
        session: AsyncSession,
    ):
        self.aviso_repository = aviso_repository
        self.session = session

    async def criar_aviso(
        self,
        user_id: UUID,
        dados: CriarAvisoDTO,
    ):
        try:
            # Descobre qual administrador está autenticado.
            result = await self.session.execute(
                select(AdministradorModel).where(
                    AdministradorModel.user_id == user_id
                )
            )
            administrador = result.scalar_one_or_none()

            if administrador is None:
                raise ValueError("Administrador não encontrado.")

            # Se o aviso for direcionado a um elenco, verifica se ele existe.
            if dados.elenco_id is not None:
                elenco = await self.session.get(
                    ElencoModel,
                    dados.elenco_id,
                )
                if elenco is None:
                    raise ValueError("Elenco não encontrado.")

            aviso = await self.aviso_repository.create_aviso(
                titulo=dados.titulo,
                conteudo=dados.conteudo,
                elenco_id=dados.elenco_id,
                administrador_id=administrador.id,
            )

            await self.session.commit()
            return aviso

        except Exception:
            await self.session.rollback()
            raise

    async def listar_avisos(self):
        return await self.aviso_repository.list_avisos()

    async def listar_avisos_por_elenco(self, elenco_id: int):
        return await self.aviso_repository.list_avisos_by_elenco(elenco_id)

    async def buscar_aviso(self, aviso_id: int):
        aviso = await self.aviso_repository.get_aviso(aviso_id)

        if aviso is None:
            raise ValueError("Aviso não encontrado.")

        return aviso

    async def atualizar_aviso(self, dados: AtualizarAvisoDTO):
        try:
            if dados.elenco_id is not None:
                elenco = await self.session.get(
                    ElencoModel,
                    dados.elenco_id,
                )
                if elenco is None:
                    raise ValueError("Elenco não encontrado.")

            aviso = await self.aviso_repository.update_aviso(
                aviso_id=dados.aviso_id,
                titulo=dados.titulo,
                conteudo=dados.conteudo,
                elenco_id=dados.elenco_id,
            )

            if aviso is None:
                raise ValueError("Aviso não encontrado.")

            await self.session.commit()
            return aviso

        except Exception:
            await self.session.rollback()
            raise

    async def excluir_aviso(self, aviso_id: int):
        try:
            excluido = await self.aviso_repository.delete_aviso(aviso_id)

            if not excluido:
                raise ValueError("Aviso não encontrado.")

            await self.session.commit()
            return True

        except Exception:
            await self.session.rollback()
            raise