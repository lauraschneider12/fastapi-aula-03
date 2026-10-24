
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models import JogoModel, ElencoModel
from app.infrastructure.database.session import get_db
from app.presentation.dependencies.admin import require_admin
from app.presentation.schemas.jogo_schemas import (
    JogoCreate,
    JogoUpdate,
    JogoRead,
)

router = APIRouter(
    prefix="/jogos",
    tags=["Jogos"],
    dependencies=[Depends(require_admin)],
)


# POST - Cadastrar jogo
@router.post(
    "/",
    response_model=JogoRead,
    status_code=status.HTTP_201_CREATED,
)
async def criar_jogo(
    dados: JogoCreate,
    db: AsyncSession = Depends(get_db),
):
    elenco = await db.get(ElencoModel, dados.elenco_id)

    if elenco is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Elenco não encontrado.",
        )

    jogo = JogoModel(**dados.model_dump())

    db.add(jogo)
    await db.commit()
    await db.refresh(jogo)

    return jogo


# GET - Listar todos os jogos
@router.get("/", response_model=list[JogoRead])
async def listar_jogos(
    db: AsyncSession = Depends(get_db),
):
    resultado = await db.scalars(
        select(JogoModel).order_by(JogoModel.data)
    )

    return resultado.all()


# GET - Buscar jogo por ID
@router.get("/{jogo_id}", response_model=JogoRead)
async def buscar_jogo(
    jogo_id: int,
    db: AsyncSession = Depends(get_db),
):
    jogo = await db.get(JogoModel, jogo_id)

    if jogo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jogo não encontrado.",
        )

    return jogo


# PUT - Atualizar jogo
@router.put("/{jogo_id}", response_model=JogoRead)
async def atualizar_jogo(
    jogo_id: int,
    dados: JogoUpdate,
    db: AsyncSession = Depends(get_db),
):
    jogo = await db.get(JogoModel, jogo_id)

    if jogo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jogo não encontrado.",
        )

    alteracoes = dados.model_dump(exclude_unset=True)

    # Se foi informado um elenco, verifica se ele existe.
    if (
        "elenco_id" in alteracoes
        and alteracoes["elenco_id"] is not None
    ):
        elenco = await db.get(
            ElencoModel,
            alteracoes["elenco_id"],
        )

        if elenco is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Elenco informado não encontrado.",
            )

    for campo, valor in alteracoes.items():
        if valor is not None or campo == "placar":
            setattr(jogo, campo, valor)

    await db.commit()
    await db.refresh(jogo)

    return jogo


# DELETE - Excluir jogo
@router.delete("/{jogo_id}")
async def excluir_jogo(
    jogo_id: int,
    db: AsyncSession = Depends(get_db),
):
    jogo = await db.get(JogoModel, jogo_id)

    if jogo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jogo não encontrado.",
        )

    await db.delete(jogo)
    await db.commit()

    return {"mensagem": "Jogo excluído com sucesso."}
