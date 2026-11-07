from app.application.dtos.treino import (
    CriarTreinoDTO,
    AtualizarTreinoDTO,
)

from app.domain.repositories.treino_repository import TreinoRepository
from app.domain.repositories.elenco_repository import ElencoRepository


class TreinoUseCases:

    def __init__(
        self,
        treino_repository: TreinoRepository,
        elenco_repository: ElencoRepository,
    ):
        self.treino_repository = treino_repository
        self.elenco_repository = elenco_repository
        self.session = treino_repository.session

    async def criar(self, dados: CriarTreinoDTO):
        try:
            elenco = await self.elenco_repository.get_elenco(
                dados.elenco_id
            )

            if elenco is None:
                raise ValueError("O elenco informado não existe.")

            treino = await self.treino_repository.create_treino(
                data=dados.data,
                local=dados.local,
                descricao=dados.descricao,
                elenco_id=dados.elenco_id,
            )

            await self.session.commit()
            return treino

        except Exception:
            await self.session.rollback()
            raise

    async def listar(self):
        return await self.treino_repository.list_treinos()

    async def listar_por_elenco(self, elenco_id: int):
        elenco = await self.elenco_repository.get_elenco(elenco_id)

        if elenco is None:
            raise ValueError("O elenco informado não existe.")

        return await self.treino_repository.list_treinos_by_elenco(
            elenco_id
        )

    async def buscar(self, treino_id: int):
        treino = await self.treino_repository.get_treino(treino_id)

        if treino is None:
            raise ValueError("Treino não encontrado.")

        return treino

    async def atualizar(self, dados: AtualizarTreinoDTO):
        try:
            treino = await self.buscar(dados.treino_id)

            data = (
                dados.data
                if dados.data is not None
                else treino.data
            )

            local = (
                dados.local
                if dados.local is not None
                else treino.local
            )

            descricao = (
                dados.descricao
                if dados.descricao is not None
                else treino.descricao
            )

            elenco_id = (
                dados.elenco_id
                if dados.elenco_id is not None
                else treino.elenco_id
            )

            elenco = await self.elenco_repository.get_elenco(elenco_id)

            if elenco is None:
                raise ValueError("O elenco informado não existe.")

            atualizado = await self.treino_repository.update_treino(
                treino_id=dados.treino_id,
                data=data,
                local=local,
                descricao=descricao,
                elenco_id=elenco_id,
            )

            if atualizado is None:
                raise ValueError("Não foi possível atualizar o treino.")

            await self.session.commit()
            return atualizado

        except Exception:
            await self.session.rollback()
            raise

    async def excluir(self, treino_id: int):
        try:
            await self.buscar(treino_id)

            excluido = await self.treino_repository.delete_treino(
                treino_id
            )

            if not excluido:
                raise ValueError("Não foi possível excluir o treino.")

            await self.session.commit()
            return True

        except Exception:
            await self.session.rollback()
            raise