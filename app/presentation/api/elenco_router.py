
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dtos.elenco import (
    CriarElencoDTO,
    AtualizarElencoDTO,
)
from app.application.use_cases.elenco import ElencoUseCases
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.elenco_repository_impl import (
    ElencoRepositoryImpl,
)
from app.presentation.dependencies.admin import require_admin
from app.presentation.schemas.elenco_schemas import (
    ElencoCreate,
    ElencoUpdate,
    ElencoRead,
)

router = APIRouter(
    prefix="/elencos",
    tags=["Elencos"],
    dependencies=[Depends(require_admin)],
)


def get_elenco_use_cases(
    db: AsyncSession = Depends(get_db),
) -> ElencoUseCases:
    repository = ElencoRepositoryImpl(db)
    return ElencoUseCases(repository)


@router.post(
    "/",
    response_model=ElencoRead,
    status_code=status.HTTP_201_CREATED,
)
async def criar_elenco(
    dados: ElencoCreate,
    use_cases: ElencoUseCases = Depends(get_elenco_use_cases),
):
    try:
        dto = CriarElencoDTO(
            ano=dados.ano,
            status=dados.status,
        )
        return await use_cases.criar(dto)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.get("/", response_model=list[ElencoRead])
async def listar_elencos(
    use_cases: ElencoUseCases = Depends(get_elenco_use_cases),
):
    return await use_cases.listar()


@router.get("/{elenco_id}", response_model=ElencoRead)
async def buscar_elenco(
    elenco_id: int,
    use_cases: ElencoUseCases = Depends(get_elenco_use_cases),
):
    try:
        return await use_cases.buscar(elenco_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.put("/{elenco_id}", response_model=ElencoRead)
async def atualizar_elenco(
    elenco_id: int,
    dados: ElencoUpdate,
    use_cases: ElencoUseCases = Depends(get_elenco_use_cases),
):
    try:
        dto = AtualizarElencoDTO(
            elenco_id=elenco_id,
            ano=dados.ano,
            status=dados.status,
        )
        return await use_cases.atualizar(dto)
    except ValueError as exc:
        mensagem = str(exc)
        codigo = (
            status.HTTP_409_CONFLICT
            if "ano" in mensagem.lower()
            else status.HTTP_404_NOT_FOUND
        )
        raise HTTPException(
            status_code=codigo,
            detail=mensagem,
        ) from exc


@router.delete("/{elenco_id}")
async def excluir_elenco(
    elenco_id: int,
    use_cases: ElencoUseCases = Depends(get_elenco_use_cases),
):
    try:
        await use_cases.excluir(elenco_id)
        return {"mensagem": "Elenco excluído com sucesso."}
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
