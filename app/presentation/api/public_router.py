from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models import (
    JogoModel,
    GolModel,
    ElencoModel,
    AtletaModel,
    AtletaElencoModel,
    CartaoModel,
)
from app.infrastructure.database.session import get_db


router = APIRouter(
    prefix="/publico",
    tags=["Site público"],
)


def converter_lista(registros):
    """Converte os registros do banco em dicionários."""
    return [
        {
            coluna.name: getattr(registro, coluna.name)
            for coluna in type(registro).__table__.columns
        }
        for registro in registros
    ]


@router.get("/jogos")
async def listar_jogos_publicos(
    db: AsyncSession = Depends(get_db),
):
    # Busca todos os jogos
    resultado = await db.execute(
        select(JogoModel).order_by(JogoModel.data)
    )

    jogos = resultado.scalars().all()

    # Busca os gols e os nomes das atletas
    resultado_gols = await db.execute(
        select(
            GolModel.id_jogo,
            GolModel.id_jogador,
            AtletaModel.nome,
        )
        .outerjoin(
            AtletaModel,
            AtletaModel.id == GolModel.id_jogador,
        )
    )

    registros_gols = resultado_gols.all()

    # Organiza os gols por jogo e por atleta
    gols_por_jogo = {}

    for id_jogo, id_jogador, nome in registros_gols:

        if id_jogo not in gols_por_jogo:
            gols_por_jogo[id_jogo] = {}

        if id_jogador not in gols_por_jogo[id_jogo]:
            gols_por_jogo[id_jogo][id_jogador] = {
                "id_jogador": id_jogador,
                "nome": (
                    "Adversário"
                    if id_jogador == 100
                    else nome or "Atleta não encontrada"
                ),
                "quantidade": 0,
            }

        gols_por_jogo[id_jogo][id_jogador]["quantidade"] += 1

    # Monta a resposta com os dados do jogo e seus gols
    return [
        {
            **{
                coluna.name: getattr(jogo, coluna.name)
                for coluna in JogoModel.__table__.columns
            },
            "gols": list(
                gols_por_jogo.get(jogo.id, {}).values()
            ),
        }
        for jogo in jogos
    ]


@router.get("/elencos")
async def listar_elencos_publicos(
    db: AsyncSession = Depends(get_db),
):
    consulta = select(ElencoModel).options(
        selectinload(ElencoModel.atletas).selectinload(
            AtletaElencoModel.atleta
        )
    )

    resultado = await db.execute(consulta)
    elencos = resultado.scalars().all()

    return [
        {
            "id": elenco.id,
            "ano": elenco.ano,
            "status": elenco.status,
            "atletas": [
                {
                    "id": relacao.atleta.id,
                    "nome": relacao.atleta.nome,
                    "posicao": relacao.atleta.posicao,
                    "numero": relacao.atleta.numero,
                    "status": relacao.atleta.status,
                }
                for relacao in elenco.atletas
                if relacao.atleta.status
            ],
        }
        for elenco in elencos

    ]


@router.get("/atletas")
async def listar_atletas_publicos(
    db: AsyncSession = Depends(get_db),
):
    resultado = await db.execute(select(AtletaModel))

    atletas = resultado.scalars().all()

    return converter_lista(atletas)
@router.get("/atletas/{atleta_id}/estatisticas")
async def estatisticas_atleta_publicas(
    atleta_id: int,
    db: AsyncSession = Depends(get_db),
):
    # Busca a atleta
    resultado = await db.execute(
        select(AtletaModel).where(
            AtletaModel.id == atleta_id,
            AtletaModel.status == True,
        )
    )

    atleta = resultado.scalar_one_or_none()

    if atleta is None:
        return {
            "erro": "Atleta não encontrada."
        }

    # Busca todos os elencos ativos aos quais a atleta pertence
    resultado = await db.execute(
        select(
            ElencoModel.id,
            ElencoModel.ano,
        )
        .join(
            AtletaElencoModel,
            AtletaElencoModel.elenco_id == ElencoModel.id,
        )
        .where(
            AtletaElencoModel.atleta_id == atleta_id,
        )
        .order_by(ElencoModel.ano)
    )

    elencos = resultado.all()

    temporadas = []

    for elenco_id, ano in elencos:

        # Conta as partidas do elenco
        resultado_jogos = await db.execute(
            select(func.count(JogoModel.id))
            .where(JogoModel.elenco_id == elenco_id)
        )

        partidas = resultado_jogos.scalar_one()

        # Conta os gols da atleta nos jogos desse elenco
        resultado_gols = await db.execute(
            select(func.count(GolModel.id_gol))
            .join(
                JogoModel,
                JogoModel.id == GolModel.id_jogo,
            )
            .where(
                JogoModel.elenco_id == elenco_id,
                GolModel.id_jogador == atleta_id,
            )
        )

        gols = resultado_gols.scalar_one()

        # Conta os cartões da atleta nos jogos desse elenco
        resultado_cartoes = await db.execute(
            select(func.count(CartaoModel.id_cartao))
            .join(
                JogoModel,
                JogoModel.id == CartaoModel.id_jogo,
            )
            .where(
                JogoModel.elenco_id == elenco_id,
                CartaoModel.id_jogador == atleta_id,
            )
        )

        cartoes = resultado_cartoes.scalar_one()

        temporadas.append({
            "elenco_id": elenco_id,
            "ano": ano,
            "gols": gols,
            "cartoes": cartoes,
            "partidas": partidas,
        })

    return {
        "atleta_id": atleta.id,
        "nome": atleta.nome,
        "temporadas": temporadas,
    }