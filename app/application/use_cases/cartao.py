
from app.application.dtos.cartao import (
    CriarCartaoDTO,
    AtualizarCartaoDTO,
)

from app.domain.repositories.cartao_repository import CartaoRepository
from app.domain.repositories.jogo_repository import JogoRepository
from app.domain.repositories.atleta_repository import AtletaRepository


class CartaoUseCases:

    def __init__(
        self,
        cartao_repository: CartaoRepository,
        jogo_repository: JogoRepository,
        atleta_repository: AtletaRepository,
    ):
        self.cartao_repository = cartao_repository
        self.jogo_repository = jogo_repository
        self.atleta_repository = atleta_repository
        self.session = cartao_repository.session

    async def validar_jogador(self, id_jogador: int) -> None:

        if id_jogador == 100:
            raise ValueError(
                "Não é possível registrar cartões para o time adversário."
            )

        atleta = await self.atleta_repository.get_atleta(id_jogador)

        if atleta is None:
            raise ValueError("Atleta não encontrada.")

        if not atleta.status:
            raise ValueError("Esta atleta está desativada.")

    async def criar(self, dados: CriarCartaoDTO):
        try:
            jogo = await self.jogo_repository.get_jogo(dados.id_jogo)

            if jogo is None:
                raise ValueError("Jogo não encontrado.")

            await self.validar_jogador(dados.id_jogador)

            cartao = await self.cartao_repository.create_cartao(
                tipo=dados.tipo,
                id_jogo=dados.id_jogo,
                id_jogador=dados.id_jogador,
            )

            await self.session.commit()
            return cartao

        except Exception:
            await self.session.rollback()
            raise

    async def listar(self):
        return await self.cartao_repository.list_cartoes()

    async def buscar(self, id_cartao: int):
        cartao = await self.cartao_repository.get_cartao(id_cartao)

        if cartao is None:
            raise ValueError("Cartão não encontrado.")

        return cartao

    async def atualizar(self, dados: AtualizarCartaoDTO):
        try:
            await self.buscar(dados.id_cartao)

            jogo = await self.jogo_repository.get_jogo(dados.id_jogo)

            if jogo is None:
                raise ValueError("Jogo não encontrado.")

            await self.validar_jogador(dados.id_jogador)

            atualizado = await self.cartao_repository.update_cartao(
                id_cartao=dados.id_cartao,
                tipo=dados.tipo,
                id_jogo=dados.id_jogo,
                id_jogador=dados.id_jogador,
            )

            if atualizado is None:
                raise ValueError("Não foi possível atualizar o cartão.")

            await self.session.commit()
            return atualizado

        except Exception:
            await self.session.rollback()
            raise

    async def excluir(self, id_cartao: int):
        try:
            await self.buscar(id_cartao)

            excluido = await self.cartao_repository.delete_cartao(id_cartao)

            if not excluido:
                raise ValueError("Não foi possível excluir o cartão.")

            await self.session.commit()
            return True

        except Exception:
            await self.session.rollback()
            raise
