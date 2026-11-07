
from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dtos.gol import (
    CriarGolDTO,
    AtualizarGolDTO,
)
from app.application.use_cases.gol import GolUseCases

from app.presentation.dependencies.admin import require_admin
from app.presentation.dependencies.use_cases import get_gol_use_cases

from app.presentation.schemas.gol_schemas import (
    GolCreate,
    GolUpdate,
    GolResponse,
)


router = APIRouter(
    prefix="/gols",
    tags=["Gols"],
    dependencies=[Depends(require_admin)],
)


@router.post("/", response_model=GolResponse, status_code=status.HTTP_201_CREATED)
async def criar_gol(
    dados: GolCreate,
    use_cases: GolUseCases = Depends(get_gol_use_cases),
):
    try:
        dto = CriarGolDTO(**dados.model_dump())
        return await use_cases.criar(dto)

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro),
        )


@router.get("/", response_model=list[GolResponse])
async def listar_gols(
    use_cases: GolUseCases = Depends(get_gol_use_cases),
):
    return await use_cases.listar()


@router.get("/{id_gol}", response_model=GolResponse)
async def buscar_gol(
    id_gol: int,
    use_cases: GolUseCases = Depends(get_gol_use_cases),
):
    try:
        return await use_cases.buscar(id_gol)

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        )


@router.put("/{id_gol}", response_model=GolResponse)
async def atualizar_gol(
    id_gol: int,
    dados: GolUpdate,
    use_cases: GolUseCases = Depends(get_gol_use_cases),
):
    try:
        dto = AtualizarGolDTO(
            id_gol=id_gol,
            **dados.model_dump(),
        )
        return await use_cases.atualizar(dto)

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro),
        )


@router.delete("/{id_gol}")
async def excluir_gol(
    id_gol: int,
    use_cases: GolUseCases = Depends(get_gol_use_cases),
):
    try:
        await use_cases.excluir(id_gol)

        return {"mensagem": "Gol excluído com sucesso."}

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        )
