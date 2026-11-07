
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dtos.atleta import (
    CriarAtletaDTO,
    AtualizarAtletaDTO,
)
from app.application.use_cases.atleta import AtletaUseCases
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.atleta_repository_impl import (
    AtletaRepositoryImpl,
)
from app.infrastructure.repositories.user_repository_impl import (
    UserRepositoryImpl,
)
from app.presentation.dependencies.admin import require_admin
from app.presentation.schemas.atleta_schemas import (
    AtletaCreate,
    AtletaUpdate,
    AtletaRead,
)

router = APIRouter(
    prefix="/atletas",
    tags=["Atletas"],
    dependencies=[Depends(require_admin)],
)


def get_atleta_use_cases(
    db: AsyncSession = Depends(get_db),
) -> AtletaUseCases:
    atleta_repository = AtletaRepositoryImpl(db)
    user_repository = UserRepositoryImpl(db)

    return AtletaUseCases(
        atleta_repository=atleta_repository,
        user_repository=user_repository,
    )


@router.post(
    "/",
    response_model=AtletaRead,
    status_code=status.HTTP_201_CREATED,
)
async def criar_atleta(
    dados: AtletaCreate,
    use_cases: AtletaUseCases = Depends(get_atleta_use_cases),
):
    try:
        dto = CriarAtletaDTO(
            nome=dados.nome,
            posicao=dados.posicao,
            numero=dados.numero,
            email=dados.email,
            senha=dados.senha,
        )
        return await use_cases.criar(dto)

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(erro),
        ) from erro


@router.get("/", response_model=list[AtletaRead])
async def listar_atletas(
    use_cases: AtletaUseCases = Depends(get_atleta_use_cases),
):
    return await use_cases.listar()


@router.get("/{atleta_id}", response_model=AtletaRead)
async def buscar_atleta(
    atleta_id: int,
    use_cases: AtletaUseCases = Depends(get_atleta_use_cases),
):
    try:
        return await use_cases.buscar(atleta_id)
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        ) from erro


@router.put("/{atleta_id}", response_model=AtletaRead)
async def atualizar_atleta(
    atleta_id: int,
    dados: AtletaUpdate,
    use_cases: AtletaUseCases = Depends(get_atleta_use_cases),
):
    try:
        dto = AtualizarAtletaDTO(
            atleta_id=atleta_id,
            nome=dados.nome,
            posicao=dados.posicao,
            numero=dados.numero,
            status=dados.status,
        )
        return await use_cases.atualizar(dto)

    except ValueError as erro:
        mensagem = str(erro)
        codigo = (
            status.HTTP_404_NOT_FOUND
            if "não encontrado" in mensagem.lower()
            else status.HTTP_409_CONFLICT
        )
        raise HTTPException(
            status_code=codigo,
            detail=mensagem,
        ) from erro


@router.delete("/{atleta_id}")
async def excluir_atleta(
    atleta_id: int,
    use_cases: AtletaUseCases = Depends(get_atleta_use_cases),
):
    try:
        await use_cases.excluir(atleta_id)
        return {"mensagem": "Atleta desativado com sucesso."}

    except ValueError as erro:
        mensagem = str(erro)
        codigo = (
            status.HTTP_404_NOT_FOUND
            if "não encontrado" in mensagem.lower()
            else status.HTTP_409_CONFLICT
        )
        raise HTTPException(
            status_code=codigo,
            detail=mensagem,
        ) from erro
