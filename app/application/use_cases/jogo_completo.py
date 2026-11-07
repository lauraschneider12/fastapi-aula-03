
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dtos.jogo_completo import (
    CriarJogoCompletoDTO,
)
from app.domain.entities.cartao import TipoCartao


class JogoCompletoUseCase:

    def __init__(
        self,
        jogo_repository,
        elenco_repository,
        gol_repository,
        cartao_repository,
        atleta_repository,
    ):
        self.jogo_repository = jogo_repository
        self.elenco_repository = elenco_repository
        self.gol_repository = gol_repository
        self.cartao_repository = cartao_repository
        self.atleta_repository = atleta_repository

        # Todos os repositórios utilizam a mesma sessão.
        self.session: AsyncSession = jogo_repository.session

    async def executar(self, dto: CriarJogoCompletoDTO):
        try:
            # 1. Verificar se o elenco existe.
            elenco = await self.elenco_repository.get_elenco(
                dto.elenco_id
            )

            if not elenco:
                raise ValueError("Elenco não encontrado.")

            # 2. Validar os jogadores responsáveis pelos gols.
            for gol in dto.gols:

                # ID 100 representa um gol do time adversário.
                if gol.id_jogador == 100:
                    continue

                atleta = await self.atleta_repository.get_atleta(
                    gol.id_jogador
                )

                if not atleta:
                    raise ValueError(
                        f"Atleta {gol.id_jogador} não encontrada."
                    )

                if not atleta.status:
                    raise ValueError(
                        f"Atleta {gol.id_jogador} está inativa."
                    )

            # 3. Validar os jogadores responsáveis pelos cartões.
            for cartao in dto.cartoes:

                # O adversário não pode receber cartão.
                if cartao.id_jogador == 100:
                    raise ValueError(
                        "Não é permitido atribuir cartão ao adversário."
                    )

                atleta = await self.atleta_repository.get_atleta(
                    cartao.id_jogador
                )

                if not atleta:
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

            # 4. Calcular o placar a partir dos gols registrados.
            gol_local = sum(
                1 for gol in dto.gols
                if gol.id_jogador != 100
            )

            gol_visitante = sum(
                1 for gol in dto.gols
                if gol.id_jogador == 100
            )

            # 5. Criar o jogo.
            jogo = await self.jogo_repository.create_jogo(
                local=dto.local,
                time_adversario=dto.time_adversario,
                data=dto.data,
                elenco_id=dto.elenco_id,
                gol_local=gol_local,
                gol_visitante=gol_visitante,
            )

            # 6. Registrar os gols relacionados ao jogo.
            gols_criados = []

            for gol in dto.gols:
                novo_gol = await self.gol_repository.create_gol(
                    id_jogo=jogo.id,
                    id_jogador=gol.id_jogador,
                )

                gols_criados.append(novo_gol)

            # 7. Registrar os cartões relacionados ao jogo.
            cartoes_criados = []

            for cartao in dto.cartoes:
                novo_cartao = await self.cartao_repository.create_cartao(
                    tipo=cartao.tipo,
                    id_jogo=jogo.id,
                    id_jogador=cartao.id_jogador,
                )

                cartoes_criados.append(novo_cartao)

            # 8. Salvar tudo de uma única vez.
            await self.session.commit()

            return {
                "jogo": jogo,
                "gols": gols_criados,
                "cartoes": cartoes_criados,
            }

        except Exception:
            # Se qualquer operação falhar, desfaz todas as alterações.
            await self.session.rollback()
            raise
