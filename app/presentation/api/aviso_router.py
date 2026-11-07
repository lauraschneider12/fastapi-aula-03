from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from app.application.dtos.aviso import (
    CriarAvisoDTO,
    AtualizarAvisoDTO,
)

from app.application.use_cases.aviso import AvisoUseCases

from app.presentation.dependencies.use_cases import (
    get_aviso_use_cases,
)

from app.presentation.dependencies.admin import require_admin

from app.infrastructure.security.user_manager import current_active_user
from app.infrastructure.database.models import UserModel

from app.presentation.schemas.aviso_schemas import (
    CriarAvisoSchema,
    AtualizarAvisoSchema,
    AvisoRead,
)


router = APIRouter(
    prefix="/avisos",
    tags=["Avisos"],
    dependencies=[Depends(require_admin)],
)


# PUBLICAR AVISO
@router.post(
    "/",
    response_model=AvisoRead,
    status_code=status.HTTP_201_CREATED,
)
async def criar_aviso(
    dados: CriarAvisoSchema,
    usuario: UserModel = Depends(current_active_user),
    use_cases: AvisoUseCases = Depends(get_aviso_use_cases),
):
    try:
        dto = CriarAvisoDTO(
            titulo=dados.titulo,
            conteudo=dados.conteudo,
            elenco_id=dados.elenco_id,
        )

        return await use_cases.criar_aviso(
            user_id=usuario.id,
            dados=dto,
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro),
        )


# LISTAR TODOS OS AVISOS
@router.get("/", response_model=list[AvisoRead])
async def listar_avisos(
    use_cases: AvisoUseCases = Depends(get_aviso_use_cases),
):
    return await use_cases.listar_avisos()


# BUSCAR AVISO POR ID
@router.get("/{aviso_id}", response_model=AvisoRead)
async def buscar_aviso(
    aviso_id: int,
    use_cases: AvisoUseCases = Depends(get_aviso_use_cases),
):
    try:
        return await use_cases.buscar_aviso(aviso_id)

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        )


# ATUALIZAR AVISO
@router.put("/{aviso_id}", response_model=AvisoRead)
async def atualizar_aviso(
    aviso_id: int,
    dados: AtualizarAvisoSchema,
    use_cases: AvisoUseCases = Depends(get_aviso_use_cases),
):
    try:
        dto = AtualizarAvisoDTO(
            aviso_id=aviso_id,
            titulo=dados.titulo,
            conteudo=dados.conteudo,
            elenco_id=dados.elenco_id,
        )

        return await use_cases.atualizar_aviso(dto)

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        )


# EXCLUIR AVISO
@router.delete("/{aviso_id}")
async def excluir_aviso(
    aviso_id: int,
    use_cases: AvisoUseCases = Depends(get_aviso_use_cases),
):
    try:
        await use_cases.excluir_aviso(aviso_id)

        return {"mensagem": "Aviso excluído com sucesso."}

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        )