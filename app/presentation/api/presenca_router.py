
from fastapi import APIRouter, Depends, HTTPException, status

from app.infrastructure.database.models import UserModel
from app.infrastructure.security.user_manager import current_active_user

from app.presentation.dependencies.admin import require_admin
from app.presentation.dependencies.use_cases import get_presenca_use_cases

from app.application.use_cases.presenca import PresencaUseCases
from app.application.dtos.presenca import (
    AtualizarConfirmacaoDTO,
    AtualizarPresenteDTO,
)

from app.presentation.schemas.presenca_schemas import (
    AtualizarConfirmacaoSchema,
    AtualizarPresenteSchema,
    PresencaRead,
)

router = APIRouter(
    prefix="/presencas",
    tags=["Presenças"],
)


# ATLETA: confirmar a própria presença
@router.post(
    "/confirmar",
    response_model=PresencaRead,
)
async def confirmar_presenca(
    dados: AtualizarConfirmacaoSchema,
    usuario: UserModel = Depends(current_active_user),
    use_cases: PresencaUseCases = Depends(get_presenca_use_cases),
):
    try:
        dto = AtualizarConfirmacaoDTO(
            treino_id=dados.treino_id,
            confirmacao=dados.confirmacao,
        )

        return await use_cases.confirmar_presenca(usuario.id, dto)

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro),
        )


# ATLETA: consultar as próprias presenças
@router.get(
    "/minhas",
    response_model=list[PresencaRead],
)
async def listar_minhas_presencas(
    usuario: UserModel = Depends(current_active_user),
    use_cases: PresencaUseCases = Depends(get_presenca_use_cases),
):
    try:
        return await use_cases.listar_minhas(usuario.id)

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        )


# ADMINISTRADOR: registrar a presença real de uma atleta
@router.put(
    "/registrar",
    response_model=PresencaRead,
    dependencies=[Depends(require_admin)],
)
async def registrar_presenca(
    dados: AtualizarPresenteSchema,
    use_cases: PresencaUseCases = Depends(get_presenca_use_cases),
):
    try:
        dto = AtualizarPresenteDTO(
            atleta_id=dados.atleta_id,
            treino_id=dados.treino_id,
            presente=dados.presente,
        )

        return await use_cases.registrar_presente(dto)

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro),
        )


# ADMINISTRADOR: consultar as presenças de um treino
@router.get(
    "/treino/{treino_id}",
    response_model=list[PresencaRead],
    dependencies=[Depends(require_admin)],
)
async def listar_presencas_treino(
    treino_id: int,
    use_cases: PresencaUseCases = Depends(get_presenca_use_cases),
):
    try:
        return await use_cases.listar_por_treino(treino_id)

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        )
