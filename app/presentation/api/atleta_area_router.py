
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_db
from app.infrastructure.database.models import (
    AtletaModel,
    AtletaElencoModel,
    ElencoModel,
    TreinoModel,
    AvisoModel,
    JogoModel,
    GolModel,
    CartaoModel,
)
from app.infrastructure.security.user_manager import current_active_user


router = APIRouter(
    prefix="/area-atleta",
    tags=["Área da Atleta"],
)


async def obter_atleta(usuario, session: AsyncSession):
    """
    Busca a atleta vinculada ao usuário autenticado.
    O ID nunca é recebido do frontend.
    """

    role = getattr(usuario.role, "value", usuario.role)

    if role != "atleta":
        raise HTTPException(
            status_code=403,
            detail="Acesso permitido somente para atletas."
        )

    result = await session.execute(
        select(AtletaModel).where(
            AtletaModel.user_id == usuario.id,
            AtletaModel.status.is_(True)
        )
    )

    atleta = result.scalar_one_or_none()

    if atleta is None:
        raise HTTPException(
            status_code=404,
            detail="Atleta não encontrada para este usuário."
        )

    return atleta


@router.get("/perfil")
async def meu_perfil(
    usuario=Depends(current_active_user),
    session: AsyncSession = Depends(get_db),
):
    """
    Retorna os dados da atleta autenticada e seus elencos.
    """

    atleta = await obter_atleta(usuario, session)

    resultado = await session.execute(
        select(
            ElencoModel.id,
            ElencoModel.ano,
        )
        .join(
            AtletaElencoModel,
            AtletaElencoModel.elenco_id == ElencoModel.id,
        )
        .where(
            AtletaElencoModel.atleta_id == atleta.id
        )
        .order_by(ElencoModel.ano.desc())
    )

    elencos = resultado.all()

    return {
        "id": atleta.id,
        "nome": atleta.nome,
        "email": usuario.email,
        "posicao": atleta.posicao,
        "numero": atleta.numero,
        "elencos": [
            {
                "id": elenco_id,
                "ano": ano,
            }
            for elenco_id, ano in elencos
        ],
    }


@router.get("/estatisticas")
async def minhas_estatisticas(
    usuario=Depends(current_active_user),
    session: AsyncSession = Depends(get_db),
):
    """
    Retorna as estatísticas da atleta autenticada,
    separadas por temporada.
    """

    atleta = await obter_atleta(usuario, session)

    resultado = await session.execute(
        select(
            ElencoModel.id,
            ElencoModel.ano,
        )
        .join(
            AtletaElencoModel,
            AtletaElencoModel.elenco_id == ElencoModel.id,
        )
        .where(
            AtletaElencoModel.atleta_id == atleta.id,
        )
        .order_by(ElencoModel.ano)
    )

    elencos = resultado.all()

    temporadas = []

    for elenco_id, ano in elencos:

        # Quantidade de partidas do elenco na temporada
        resultado_jogos = await session.execute(
            select(func.count(JogoModel.id))
            .where(JogoModel.elenco_id == elenco_id)
        )

        partidas = resultado_jogos.scalar_one()

        # Gols marcados pela atleta na temporada
        resultado_gols = await session.execute(
            select(func.count(GolModel.id_gol))
            .join(
                JogoModel,
                JogoModel.id == GolModel.id_jogo,
            )
            .where(
                JogoModel.elenco_id == elenco_id,
                GolModel.id_jogador == atleta.id,
            )
        )

        gols = resultado_gols.scalar_one()

        # Cartões recebidos pela atleta na temporada
        resultado_cartoes = await session.execute(
            select(func.count(CartaoModel.id_cartao))
            .join(
                JogoModel,
                JogoModel.id == CartaoModel.id_jogo,
            )
            .where(
                JogoModel.elenco_id == elenco_id,
                CartaoModel.id_jogador == atleta.id,
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


@router.get("/treinos")
async def listar_meus_treinos(
    usuario=Depends(current_active_user),
    session: AsyncSession = Depends(get_db),
):
    """
    Lista os treinos dos elencos aos quais a atleta pertence.
    """

    atleta = await obter_atleta(usuario, session)

    result = await session.execute(
        select(AtletaElencoModel.elenco_id).where(
            AtletaElencoModel.atleta_id == atleta.id
        )
    )

    elenco_ids = result.scalars().all()

    if not elenco_ids:
        return []

    result = await session.execute(
        select(TreinoModel)
        .where(TreinoModel.elenco_id.in_(elenco_ids))
        .order_by(TreinoModel.data)
    )

    treinos = result.scalars().all()

    return [
        {
            "id": treino.id,
            "data": treino.data,
            "local": treino.local,
            "descricao": treino.descricao,
            "elenco_id": treino.elenco_id,
        }
        for treino in treinos
    ]


@router.get("/avisos")
async def listar_meus_avisos(
    usuario=Depends(current_active_user),
    session: AsyncSession = Depends(get_db),
):
    """
    Lista os avisos gerais e os avisos dos elencos da atleta.
    """

    atleta = await obter_atleta(usuario, session)

    result = await session.execute(
        select(AtletaElencoModel.elenco_id).where(
            AtletaElencoModel.atleta_id == atleta.id
        )
    )

    elenco_ids = result.scalars().all()

    if elenco_ids:
        filtro = or_(
            AvisoModel.elenco_id.in_(elenco_ids),
            AvisoModel.elenco_id.is_(None)
        )
    else:
        filtro = AvisoModel.elenco_id.is_(None)

    result = await session.execute(
        select(AvisoModel)
        .where(filtro)
        .order_by(AvisoModel.data_publicacao.desc())
    )

    avisos = result.scalars().all()

    return [
        {
            "id": aviso.id,
            "titulo": aviso.titulo,
            "conteudo": aviso.conteudo,
            "data_publicacao": aviso.data_publicacao,
            "elenco_id": aviso.elenco_id,
            "administrador_id": aviso.administrador_id,
        }
        for aviso in avisos
    ]
