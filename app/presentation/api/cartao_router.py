
from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dtos.cartao import (
    CriarCartaoDTO,
    AtualizarCartaoDTO,
)
from app.application.use_cases.cartao import CartaoUseCases

from app.presentation.dependencies.admin import require_admin
from app.presentation.dependencies.use_cases import get_cartao_use_cases

from app.presentation.schemas.cartao_schemas import (
    CartaoCreate,
    CartaoUpdate,
    CartaoResponse,
)


router = APIRouter(
    prefix="/cartoes",
    tags=["Cartões"],
    dependencies=[Depends(require_admin)],
)


@router.post("/", response_model=CartaoResponse, status_code=status.HTTP_201_CREATED)
async def criar_cartao(
    dados: CartaoCreate,
    use_cases: CartaoUseCases = Depends(get_cartao_use_cases),
):
    try:
        dto = CriarCartaoDTO(**dados.model_dump())
        return await use_cases.criar(dto)

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro),
        )


@router.get("/", response_model=list[CartaoResponse])
async def listar_cartoes(
    use_cases: CartaoUseCases = Depends(get_cartao_use_cases),
):
    return await use_cases.listar()


@router.get("/{id_cartao}", response_model=CartaoResponse)
async def buscar_cartao(
    id_cartao: int,
    use_cases: CartaoUseCases = Depends(get_cartao_use_cases),
):
    try:
        return await use_cases.buscar(id_cartao)

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        )


@router.put("/{id_cartao}", response_model=CartaoResponse)
async def atualizar_cartao(
    id_cartao: int,
    dados: CartaoUpdate,
    use_cases: CartaoUseCases = Depends(get_cartao_use_cases),
):
    try:
        dto = AtualizarCartaoDTO(
            id_cartao=id_cartao,
            **dados.model_dump(),
        )
        return await use_cases.atualizar(dto)

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro),
        )


@router.delete("/{id_cartao}")
async def excluir_cartao(
    id_cartao: int,
    use_cases: CartaoUseCases = Depends(get_cartao_use_cases),
):
    try:
        await use_cases.excluir(id_cartao)

        return {"mensagem": "Cartão excluído com sucesso."}

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        )
