from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dtos.treino import (
    CriarTreinoDTO,
    AtualizarTreinoDTO,
)

from app.application.use_cases.treino import TreinoUseCases

from app.presentation.dependencies.admin import require_admin
from app.presentation.dependencies.use_cases import get_treino_use_cases

from app.presentation.schemas.treino_schemas import (
    TreinoCreate,
    TreinoUpdate,
    TreinoRead,
)


router = APIRouter(
    prefix="/treinos",
    tags=["Treinos"],
    dependencies=[Depends(require_admin)],
)


# CADASTRAR TREINO
@router.post(
    "/",
    response_model=TreinoRead,
    status_code=status.HTTP_201_CREATED,
)
async def criar_treino(
    dados: TreinoCreate,
    use_cases: TreinoUseCases = Depends(get_treino_use_cases),
):
    try:
        dto = CriarTreinoDTO(
            data=dados.data,
            local=dados.local,
            descricao=dados.descricao,
            elenco_id=dados.elenco_id,
        )

        return await use_cases.criar(dto)

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro),
        )


# LISTAR TODOS OS TREINOS
@router.get("/", response_model=list[TreinoRead])
async def listar_treinos(
    use_cases: TreinoUseCases = Depends(get_treino_use_cases),
):
    return await use_cases.listar()


# BUSCAR TREINO
@router.get("/{treino_id}", response_model=TreinoRead)
async def buscar_treino(
    treino_id: int,
    use_cases: TreinoUseCases = Depends(get_treino_use_cases),
):
    try:
        return await use_cases.buscar(treino_id)

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        )


# LISTAR TREINOS DE UM ELENCO
@router.get("/elenco/{elenco_id}", response_model=list[TreinoRead])
async def listar_treinos_por_elenco(
    elenco_id: int,
    use_cases: TreinoUseCases = Depends(get_treino_use_cases),
):
    try:
        return await use_cases.listar_por_elenco(elenco_id)

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        )


# ATUALIZAR TREINO
@router.put("/{treino_id}", response_model=TreinoRead)
async def atualizar_treino(
    treino_id: int,
    dados: TreinoUpdate,
    use_cases: TreinoUseCases = Depends(get_treino_use_cases),
):
    try:
        dados_dict = dados.model_dump(exclude_unset=True)

        dto = AtualizarTreinoDTO(
            treino_id=treino_id,
            **dados_dict,
        )

        return await use_cases.atualizar(dto)

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro),
        )


# EXCLUIR TREINO
@router.delete("/{treino_id}", status_code=status.HTTP_204_NO_CONTENT)
async def excluir_treino(
    treino_id: int,
    use_cases: TreinoUseCases = Depends(get_treino_use_cases),
):
    try:
        await use_cases.excluir(treino_id)
        return None

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        )