
from fastapi import APIRouter, Depends, HTTPException, status
from app.application.dtos.gol import CriarGolDTO
from app.application.dtos.cartao import CriarCartaoDTO

from app.application.dtos.jogo import AtualizarJogoDTO
from app.application.dtos.jogo_completo import (
    CriarJogoCompletoDTO,
    GolJogoDTO,
    CartaoJogoDTO,
)

from app.application.use_cases.jogo import JogoUseCases
from app.application.use_cases.jogo_completo import JogoCompletoUseCase

from app.presentation.dependencies.admin import require_admin
from app.presentation.dependencies.use_cases import (
    get_jogo_use_cases,
    get_jogo_completo_use_case,
)

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


# CADASTRAR JOGO COMPLETO
@router.post(
    "/",
    response_model=JogoRead,
    status_code=status.HTTP_201_CREATED,
)
async def criar_jogo(
    dados: JogoCreate,
    use_cases: JogoCompletoUseCase = Depends(
        get_jogo_completo_use_case
    ),
):
    try:
        dto = CriarJogoCompletoDTO(
            local=dados.local,
            time_adversario=dados.time_adversario,
            data=dados.data,
            elenco_id=dados.elenco_id,
            gols=[
                GolJogoDTO(id_jogador=gol.id_jogador)
                for gol in dados.gols
            ],
            cartoes=[
                CartaoJogoDTO(
                    tipo=cartao.tipo,
                    id_jogador=cartao.id_jogador,
                )
                for cartao in dados.cartoes
            ],
        )

        resultado = await use_cases.executar(dto)

        return resultado["jogo"]

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro),
        )


# LISTAR JOGOS
@router.get("/", response_model=list[JogoRead])
async def listar_jogos(
    use_cases: JogoUseCases = Depends(get_jogo_use_cases),
):
    return await use_cases.listar()


# BUSCAR JOGO
@router.get("/{jogo_id}", response_model=JogoRead)
async def buscar_jogo(
    jogo_id: int,
    use_cases: JogoUseCases = Depends(get_jogo_use_cases),
):
    try:
        return await use_cases.buscar(jogo_id)

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        )


# ATUALIZAR JOGO
@router.put("/{jogo_id}", response_model=JogoRead)
async def atualizar_jogo(
    jogo_id: int,
    dados: JogoUpdate,
    use_cases: JogoUseCases = Depends(get_jogo_use_cases),
):
    try:
        dados_dict = dados.model_dump(exclude_unset=True)

        gols = dados_dict.pop("gols", None)
        cartoes = dados_dict.pop("cartoes", None)

        dto = AtualizarJogoDTO(
            jogo_id=jogo_id,
            **dados_dict,
            gols=(
                [
                    CriarGolDTO(
                        id_jogo=jogo_id,
                        id_jogador=gol["id_jogador"],
                    )
                    for gol in gols
                ]
                if gols is not None
                else None
            ),
            cartoes=(
                [
                    CriarCartaoDTO(
                        id_jogo=jogo_id,
                        id_jogador=cartao["id_jogador"],
                        tipo=cartao["tipo"],
                    )
                    for cartao in cartoes
                ]
                if cartoes is not None
                else None
            ),
        )

        return await use_cases.atualizar(dto)

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro),
        )