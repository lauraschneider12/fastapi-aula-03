
from collections import defaultdict
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.entities.elenco import ElencoResumo
from app.domain.entities.jogo import Jogo, GolResumo
from app.domain.entities.cartao import Cartao
from app.domain.repositories.jogo_repository import JogoRepository

from app.infrastructure.database.models import (
    JogoModel,
    GolModel,
    CartaoModel,
    AtletaModel,
)


class JogoRepositoryImpl(JogoRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def _buscar_gols_por_jogos(
        self,
        ids_jogos: list[int],
    ) -> dict[int, list[GolResumo]]:

        if not ids_jogos:
            return {}

        result = await self.session.execute(
            select(
                GolModel.id_jogo,
                GolModel.id_jogador,
                AtletaModel.nome,
            )
            .outerjoin(
                AtletaModel,
                AtletaModel.id == GolModel.id_jogador,
            )
            .where(GolModel.id_jogo.in_(ids_jogos))
        )

        contagem = defaultdict(int)
        nomes = {}

        for id_jogo, id_jogador, nome in result.all():
            chave = (id_jogo, id_jogador)

            contagem[chave] += 1

            if id_jogador == 100:
                nomes[chave] = "Adversário"
            else:
                nomes[chave] = nome or "Atleta não encontrada"

        gols_por_jogo = defaultdict(list)

        for (id_jogo, id_jogador), quantidade in contagem.items():
            gols_por_jogo[id_jogo].append(
                GolResumo(
                    id_jogador=id_jogador,
                    nome=nomes[(id_jogo, id_jogador)],
                    quantidade=quantidade,
                )
            )

        return dict(gols_por_jogo)

    async def _buscar_cartoes_por_jogos(
        self,
        ids_jogos: list[int],
    ) -> dict[int, list[Cartao]]:

        if not ids_jogos:
            return {}

        result = await self.session.execute(
            select(CartaoModel)
            .where(CartaoModel.id_jogo.in_(ids_jogos))
        )

        cartoes_por_jogo = defaultdict(list)

        for model in result.scalars().all():
            cartoes_por_jogo[model.id_jogo].append(
                Cartao(
                    id_cartao=model.id_cartao,
                    tipo=model.tipo,
                    id_jogo=model.id_jogo,
                    id_jogador=model.id_jogador,
                )
            )

        return dict(cartoes_por_jogo)

    @staticmethod
    def _to_entity(
        model: JogoModel,
        gols: list[GolResumo] | None = None,
        cartoes: list[Cartao] | None = None,
    ) -> Jogo:

        return Jogo(
            id=model.id,
            local=model.local,
            time_adversario=model.time_adversario,
            data=model.data,
            elenco_id=model.elenco_id,
            ano_elenco=ElencoResumo(
                ano=model.elenco.ano
            ),
            gol_local=model.gol_local,
            gol_visitante=model.gol_visitante,
            gols=gols or [],
            cartoes=cartoes or [],
        )

    async def create_jogo(
        self,
        local: str,
        time_adversario: str,
        data: datetime,
        elenco_id: int,
        gol_local: int,
        gol_visitante: int,
    ) -> Jogo:

        model = JogoModel(
            local=local,
            time_adversario=time_adversario,
            data=data,
            elenco_id=elenco_id,
            gol_local=gol_local,
            gol_visitante=gol_visitante,
        )

        self.session.add(model)
        await self.session.flush()

        result = await self.session.execute(
            select(JogoModel)
            .options(selectinload(JogoModel.elenco))
            .where(JogoModel.id == model.id)
        )

        model = result.scalar_one()

        return self._to_entity(model)

    async def list_jogos(self) -> list[Jogo]:

        result = await self.session.execute(
            select(JogoModel)
            .options(selectinload(JogoModel.elenco))
            .order_by(JogoModel.data)
        )

        modelos = result.scalars().all()

        ids_jogos = [jogo.id for jogo in modelos]

        gols = await self._buscar_gols_por_jogos(ids_jogos)
        cartoes = await self._buscar_cartoes_por_jogos(ids_jogos)

        return [
            self._to_entity(
                item,
                gols.get(item.id, []),
                cartoes.get(item.id, []),
            )
            for item in modelos
        ]

    async def get_jogo(self, jogo_id: int) -> Jogo | None:

        result = await self.session.execute(
            select(JogoModel)
            .options(selectinload(JogoModel.elenco))
            .where(JogoModel.id == jogo_id)
        )

        model = result.scalar_one_or_none()

        if model is None:
            return None

        gols = await self._buscar_gols_por_jogos([jogo_id])
        cartoes = await self._buscar_cartoes_por_jogos([jogo_id])

        return self._to_entity(
            model,
            gols.get(jogo_id, []),
            cartoes.get(jogo_id, []),
        )

    async def update_jogo(
        self,
        jogo_id: int,
        local: str,
        time_adversario: str,
        data: datetime,
        elenco_id: int,
        gol_local: int,
        gol_visitante: int,
    ) -> Jogo | None:

        result = await self.session.execute(
            select(JogoModel).where(
                JogoModel.id == jogo_id
            )
        )

        model = result.scalar_one_or_none()

        if model is None:
            return None

        model.local = local
        model.time_adversario = time_adversario
        model.data = data
        model.elenco_id = elenco_id
        model.gol_local = gol_local
        model.gol_visitante = gol_visitante

        await self.session.flush()

        return await self.get_jogo(jogo_id)

    async def delete_jogo(self, jogo_id: int) -> bool:

        result = await self.session.execute(
            select(JogoModel).where(
                JogoModel.id == jogo_id
            )
        )

        model = result.scalar_one_or_none()

        if model is None:
            return False

        await self.session.delete(model)
        await self.session.flush()

        return True
