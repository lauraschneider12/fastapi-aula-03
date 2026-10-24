
from app.application.dtos.jogo import (
    CriarJogoDTO,
    AtualizarJogoDTO,
)
from app.domain.repositories.jogo_repository import JogoRepository
from app.domain.repositories.elenco_repository import ElencoRepository


class JogoUseCases:
    def __init__(
        self,
        jogo_repository: JogoRepository,
        elenco_repository: ElencoRepository,
    ):
        self.jogo_repository = jogo_repository
        self.elenco_repository = elenco_repository

    async def criar(self, dados: CriarJogoDTO):
        elenco = await self.elenco_repository.get_elenco(dados.elenco_id)

        if elenco is None:
            raise ValueError("O elenco informado não existe.")

        return await self.jogo_repository.create_jogo(
            local=dados.local,
            time_adversario=dados.time_adversario,
            data=dados.data,
            elenco_id=dados.elenco_id,
            placar=dados.placar,
        )

    async def listar(self):
        return await self.jogo_repository.list_jogos()

    async def buscar(self, jogo_id: int):
        jogo = await self.jogo_repository.get_jogo(jogo_id)

        if jogo is None:
            raise ValueError("Jogo não encontrado.")

        return jogo

    async def atualizar(self, dados: AtualizarJogoDTO):
        jogo = await self.buscar(dados.jogo_id)

        local = dados.local if dados.local is not None else jogo.local
        adversario = (
            dados.time_adversario
            if dados.time_adversario is not None
            else jogo.time_adversario
        )
        data = dados.data if dados.data is not None else jogo.data
        elenco_id = (
            dados.elenco_id
            if dados.elenco_id is not None
            else jogo.elenco_id
        )
        placar = dados.placar if dados.placar is not None else jogo.placar

        elenco = await self.elenco_repository.get_elenco(elenco_id)
        if elenco is None:
            raise ValueError("O elenco informado não existe.")

        return await self.jogo_repository.update_jogo(
            jogo_id=dados.jogo_id,
            local=local,
            time_adversario=adversario,
            data=data,
            elenco_id=elenco_id,
            placar=placar,
        )

    async def excluir(self, jogo_id: int):
        await self.buscar(jogo_id)
        excluido = await self.jogo_repository.delete_jogo(jogo_id)

        if not excluido:
            raise ValueError("Não foi possível excluir o jogo.")

        return True
