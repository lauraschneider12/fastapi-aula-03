
from uuid import UUID

from app.application.dtos.atleta import (
    CriarAtletaDTO,
    AtualizarAtletaDTO,
)
from app.domain.repositories.atleta_repository import AtletaRepository
from app.domain.repositories.user_repository import UserRepository
from app.domain.entities.user import UserRole


class AtletaUseCases:
    def __init__(
        self,
        atleta_repository: AtletaRepository,
        user_repository: UserRepository,
    ):
        self.atleta_repository = atleta_repository
        self.user_repository = user_repository

    async def criar(self, dto: CriarAtletaDTO):
        existente = await self.user_repository.get_user_by_email(
            dto.email
        )

        if existente:
            raise ValueError("Este e-mail já está cadastrado.")

        usuario = await self.user_repository.create_user(
            email=dto.email,
            senha=dto.senha,
            role=UserRole.ATLETA.value,
        )

        return await self.atleta_repository.create_atleta(
            nome=dto.nome,
            posicao=dto.posicao,
            numero=dto.numero,
            user_id=usuario.id,
        )

    async def listar(self):
        return await self.atleta_repository.list_atletas()

    async def buscar(self, atleta_id: int):
        atleta = await self.atleta_repository.get_atleta(atleta_id)

        if atleta is None:
            raise ValueError("Atleta não encontrado.")

        return atleta

    async def atualizar(self, dto: AtualizarAtletaDTO):
        atleta = await self.atleta_repository.get_atleta(dto.atleta_id)

        if atleta is None:
            raise ValueError("Atleta não encontrado.")

        nome = dto.nome if dto.nome is not None else atleta.nome
        posicao = dto.posicao if dto.posicao is not None else atleta.posicao
        numero = dto.numero if dto.numero is not None else atleta.numero

        atualizado = await self.atleta_repository.update_atleta(
            atleta_id=dto.atleta_id,
            nome=nome,
            posicao=posicao,
            numero=numero,
        )

        if atualizado is None:
            raise ValueError("Não foi possível atualizar o atleta.")

        return atualizado

    async def excluir(self, atleta_id: int) -> bool:
        atleta = await self.atleta_repository.get_atleta(atleta_id)

        if atleta is None:
            raise ValueError("Atleta não encontrado.")

        return await self.atleta_repository.delete_atleta(atleta_id)
