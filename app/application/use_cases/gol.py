
from app.application.dtos.gol import (
    CriarGolDTO,
    AtualizarGolDTO,
)

from app.domain.repositories.gol_repository import GolRepository
from app.domain.repositories.jogo_repository import JogoRepository
from app.domain.repositories.atleta_repository import AtletaRepository


class GolUseCases:

    def __init__(
        self,
        gol_repository: GolRepository,
        jogo_repository: JogoRepository,
        atleta_repository: AtletaRepository,
    ):
        self.gol_repository = gol_repository
        self.jogo_repository = jogo_repository
        self.atleta_repository = atleta_repository
        self.session = gol_repository.session

    async def validar_jogador(self, id_jogador: int) -> None:

        # ID 100 representa o time adversário.
        if id_jogador == 100:
            return

        atleta = await self.atleta_repository.get_atleta(id_jogador)

        if atleta is None:
            raise ValueError("Atleta não encontrada.")

        if not atleta.status:
            raise ValueError("Esta atleta está desativada.")

    async def criar(self, dados: CriarGolDTO):
        try:
            jogo = await self.jogo_repository.get_jogo(dados.id_jogo)

            if jogo is None:
                raise ValueError("Jogo não encontrado.")

            await self.validar_jogador(dados.id_jogador)

            gol = await self.gol_repository.create_gol(
                id_jogo=dados.id_jogo,
                id_jogador=dados.id_jogador,
            )

            await self.session.commit()
            return gol

        except Exception:
            await self.session.rollback()
            raise

    async def listar(self):
        return await self.gol_repository.list_gols()

    async def buscar(self, id_gol: int):
        gol = await self.gol_repository.get_gol(id_gol)

        if gol is None:
            raise ValueError("Gol não encontrado.")

        return gol

    async def atualizar(self, dados: AtualizarGolDTO):
        try:
            await self.buscar(dados.id_gol)

            jogo = await self.jogo_repository.get_jogo(dados.id_jogo)

            if jogo is None:
                raise ValueError("Jogo não encontrado.")

            await self.validar_jogador(dados.id_jogador)

            atualizado = await self.gol_repository.update_gol(
                id_gol=dados.id_gol,
                id_jogo=dados.id_jogo,
                id_jogador=dados.id_jogador,
            )

            if atualizado is None:
                raise ValueError("Não foi possível atualizar o gol.")

            await self.session.commit()
            return atualizado

        except Exception:
            await self.session.rollback()
            raise

    async def excluir(self, id_gol: int):
        try:
            await self.buscar(id_gol)

            excluido = await self.gol_repository.delete_gol(id_gol)

            if not excluido:
                raise ValueError("Não foi possível excluir o gol.")

            await self.session.commit()
            return True

        except Exception:
            await self.session.rollback()
            raise
