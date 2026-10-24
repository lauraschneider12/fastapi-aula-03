
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import UserRole
from app.infrastructure.database.models import AtletaModel, UserModel
from app.infrastructure.database.session import get_db
from app.infrastructure.security.password_hasher import password_helper
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


# POST - Cadastrar atleta
@router.post(
    "/",
    response_model=AtletaRead,
    status_code=status.HTTP_201_CREATED,
)
async def criar_atleta(
    dados: AtletaCreate,
    db: AsyncSession = Depends(get_db),
):
    usuario_existente = await db.scalar(
        select(UserModel).where(UserModel.email == dados.email)
    )

    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este e-mail já está cadastrado.",
        )

    usuario = UserModel(
        email=dados.email,
        hashed_password=password_helper.hash(dados.senha),
        role=UserRole.ATLETA.value,
        is_active=True,
        is_verified=True,
    )

    try:
        db.add(usuario)
        await db.flush()

        atleta = AtletaModel(
            nome=dados.nome,
            posicao=dados.posicao,
            numero=dados.numero,
            user_id=usuario.id,
        )

        db.add(atleta)
        await db.commit()
        await db.refresh(atleta)

        return atleta

    except Exception:
        await db.rollback()
        raise


# GET - Listar todos os atletas
@router.get("/", response_model=list[AtletaRead])
async def listar_atletas(
    db: AsyncSession = Depends(get_db),
):
    resultado = await db.scalars(
        select(AtletaModel).order_by(AtletaModel.id)
    )
    return resultado.all()


# GET - Buscar atleta por ID
@router.get("/{atleta_id}", response_model=AtletaRead)
async def buscar_atleta(
    atleta_id: int,
    db: AsyncSession = Depends(get_db),
):
    atleta = await db.get(AtletaModel, atleta_id)

    if atleta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Atleta não encontrado.",
        )

    return atleta


# PUT - Atualizar atleta
@router.put("/{atleta_id}", response_model=AtletaRead)
async def atualizar_atleta(
    atleta_id: int,
    dados: AtletaUpdate,
    db: AsyncSession = Depends(get_db),
):
    atleta = await db.get(AtletaModel, atleta_id)

    if atleta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Atleta não encontrado.",
        )

    alteracoes = dados.model_dump(exclude_unset=True)

    for campo, valor in alteracoes.items():
        if valor is not None or campo == "status":
            setattr(atleta, campo, valor)

    await db.commit()
    await db.refresh(atleta)

    return atleta


# DELETE - Desativar atleta
@router.delete("/{atleta_id}")
async def excluir_atleta(
    atleta_id: int,
    db: AsyncSession = Depends(get_db),
):
    atleta = await db.get(AtletaModel, atleta_id)

    if atleta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Atleta não encontrado.",
        )

    # Desativa o perfil sem apagar a conta de usuário.
    atleta.status = False

    await db.commit()

    return {"mensagem": "Atleta desativado com sucesso."}
