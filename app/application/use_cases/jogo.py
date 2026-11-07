
from app.application.dtos.jogo import (
    CriarJogoDTO,
    AtualizarJogoDTO,
)
from app.domain.repositories.jogo_repository import JogoRepository
from app.domain.repositories.elenco_repository import ElencoRepository
from app.domain.entities.cartao import TipoCartao


class JogoUseCases:

    def __init__(
        self,
        jogo_repository: JogoRepository,
        elenco_repository: ElencoRepository,
        gol_repository,
        cartao_repository,
        atleta_repository,
    ):
        self.jogo_repository = jogo_repository
        self.elenco_repository = elenco_repository
        self.gol_repository = gol_repository
        self.cartao_repository = cartao_repository
        self.atleta_repository = atleta_repository
        self.session = jogo_repository.session

    async def criar(self, dados: CriarJogoDTO):
        try:
            elenco = await self.elenco_repository.get_elenco(
                dados.elenco_id
            )

            if elenco is None:
                raise ValueError("O elenco informado não existe.")

            jogo = await self.jogo_repository.create_jogo(
                local=dados.local,
                time_adversario=dados.time_adversario,
                data=dados.data,
                elenco_id=dados.elenco_id,
                gol_local=0,
                gol_visitante=0,
            )

            await self.session.commit()
            return jogo

        except Exception:
            await self.session.rollback()
            raise

    async def listar(self):
        return await self.jogo_repository.list_jogos()

    async def buscar(self, jogo_id: int):
        jogo = await self.jogo_repository.get_jogo(jogo_id)

        if jogo is None:
            raise ValueError("Jogo não encontrado.")

        return jogo

    async def atualizar(self, dados: AtualizarJogoDTO):
        try:
            jogo = await self.buscar(dados.jogo_id)

            local = (
                dados.local
                if dados.local is not None
                else jogo.local
            )

            adversario = (
                dados.time_adversario
                if dados.time_adversario is not None
                else jogo.time_adversario
            )

            data = (
                dados.data
                if dados.data is not None
                else jogo.data
            )

            elenco_id = (
                dados.elenco_id
                if dados.elenco_id is not None
                else jogo.elenco_id
            )

            elenco = await self.elenco_repository.get_elenco(elenco_id)

            if elenco is None:
                raise ValueError("O elenco informado não existe.")

            gols_atuais = await self.gol_repository.list_gols()
            cartoes_atuais = await self.cartao_repository.list_cartoes()

            gols_jogo = [
                gol for gol in gols_atuais
                if gol.id_jogo == dados.jogo_id
            ]

            cartoes_jogo = [
                cartao for cartao in cartoes_atuais
                if cartao.id_jogo == dados.jogo_id
            ]

            if dados.gols is not None:
                for gol in dados.gols:
                    if gol.id_jogador == 100:
                        continue

                    atleta = await self.atleta_repository.get_atleta(
                        gol.id_jogador
                    )

                    if atleta is None:
                        raise ValueError(
                            f"Atleta {gol.id_jogador} não encontrada."
                        )

                    if not atleta.status:
                        raise ValueError(
                            f"Atleta {gol.id_jogador} está inativa."
                        )

                for gol in gols_jogo:
                    await self.gol_repository.delete_gol(gol.id_gol)

                for gol in dados.gols:
                    await self.gol_repository.create_gol(
                        id_jogo=dados.jogo_id,
                        id_jogador=gol.id_jogador,
                    )

                gols_para_calcular = dados.gols

            else:
                gols_para_calcular = gols_jogo

            if dados.cartoes is not None:
                for cartao in dados.cartoes:
                    if cartao.id_jogador == 100:
                        raise ValueError(
                            "Não é permitido atribuir cartão ao adversário."
                        )

                    atleta = await self.atleta_repository.get_atleta(
                        cartao.id_jogador
                    )

                    if atleta is None:
                        raise ValueError(
                            f"Atleta {cartao.id_jogador} não encontrada."
                        )

                    if not atleta.status:
                        raise ValueError(
                            f"Atleta {cartao.id_jogador} está inativa."
                        )

                    if cartao.tipo not in (
                        TipoCartao.AMARELO,
                        TipoCartao.VERMELHO,
                    ):
                        raise ValueError("Tipo de cartão inválido.")

                for cartao in cartoes_jogo:
                    await self.cartao_repository.delete_cartao(
                        cartao.id_cartao
                    )

                for cartao in dados.cartoes:
                    await self.cartao_repository.create_cartao(
                        tipo=cartao.tipo,
                        id_jogo=dados.jogo_id,
                        id_jogador=cartao.id_jogador,
                    )

            gol_local = sum(
                1 for gol in gols_para_calcular
                if gol.id_jogador != 100
            )

            gol_visitante = sum(
                1 for gol in gols_para_calcular
                if gol.id_jogador == 100
            )

            atualizado = await self.jogo_repository.update_jogo(
                jogo_id=dados.jogo_id,
                local=local,
                time_adversario=adversario,
                data=data,
                elenco_id=elenco_id,
                gol_local=gol_local,
                gol_visitante=gol_visitante,
            )

            await self.session.commit()
            return atualizado

        except Exception:
            await self.session.rollback()
            raise

    async def excluir(self, jogo_id: int):
        try:
            await self.buscar(jogo_id)

            excluido = await self.jogo_repository.delete_jogo(jogo_id)

            if not excluido:
                raise ValueError("Não foi possível excluir o jogo.")

            await self.session.commit()
            return True

        except Exception:
            await self.session.rollback()
            raise
