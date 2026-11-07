from app.application.dtos.atleta import (
    CriarAtletaDTO,
    AtualizarAtletaDTO,
)
from app.domain.repositories.atleta_repository import AtletaRepository
from app.domain.repositories.user_repository import UserRepository
from app.domain.entities.user import UserRole
from app.infrastructure.email.email_service import enviar_credenciais


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

        atleta = await self.atleta_repository.create_atleta(
            nome=dto.nome,
            posicao=dto.posicao,
            numero=dto.numero,
            user_id=usuario.id,
        )

        try:
            await enviar_credenciais(
                email_destinatario=dto.email,
                senha=dto.senha,
            )
        except Exception:
            print(
                "Atleta cadastrada, mas não foi possível enviar o e-mail."
            )

        return atleta

    async def listar(self):
        return await self.atleta_repository.list_atletas()

    async def buscar(self, atleta_id: int):
        atleta = await self.atleta_repository.get_atleta(atleta_id)

        if atleta is None:
            raise ValueError("Atleta não encontrado.")

        return atleta

    async def atualizar(self, dto: AtualizarAtletaDTO):
        atleta = await self.buscar(dto.atleta_id)

        nome = dto.nome if dto.nome is not None else atleta.nome
        posicao = dto.posicao if dto.posicao is not None else atleta.posicao
        numero = dto.numero if dto.numero is not None else atleta.numero
        status = dto.status if dto.status is not None else atleta.status

        atualizado = await self.atleta_repository.update_atleta(
            atleta_id=dto.atleta_id,
            nome=nome,
            posicao=posicao,
            numero=numero,
            status=status,
        )

        if atualizado is None:
            raise ValueError("Não foi possível atualizar o atleta.")

        return atualizado

    async def excluir(self, atleta_id: int) -> bool:
        atleta = await self.buscar(atleta_id)

        if not atleta.status:
            raise ValueError("Este atleta já está desativado.")

        return await self.atleta_repository.delete_atleta(atleta_id)
