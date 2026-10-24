
from uuid import UUID

from app.application.dtos.user import (
    CriarUserDTO,
    AtualizarUserDTO,
)
from app.domain.repositories.user_repository import UserRepository


class UserUseCases:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def criar(self, dados: CriarUserDTO):
        existente = await self.repository.get_user_by_email(dados.email)

        if existente is not None:
            raise ValueError("Já existe um usuário com esse e-mail.")

        return await self.repository.create_user(
            email=dados.email,
            senha=dados.senha,
            role=dados.role,
        )

    async def buscar(self, user_id: UUID):
        user = await self.repository.get_user_by_id(user_id)

        if user is None:
            raise ValueError("Usuário não encontrado.")

        return user

    async def buscar_por_email(self, email: str):
        user = await self.repository.get_user_by_email(email)

        if user is None:
            raise ValueError("Usuário não encontrado.")

        return user

    async def atualizar(self, dados: AtualizarUserDTO):
        user = await self.buscar(dados.user_id)

        email = dados.email if dados.email is not None else user.email
        role_atual = getattr(user.role, "value", user.role)
        role = dados.role if dados.role is not None else role_atual

        if email != user.email:
            existente = await self.repository.get_user_by_email(email)

            if existente is not None:
                raise ValueError("Já existe um usuário com esse e-mail.")

        return await self.repository.update_user(
            user_id=dados.user_id,
            email=email,
            role=role,
        )

    async def excluir(self, user_id: UUID):
        await self.buscar(user_id)
        excluido = await self.repository.delete_user(user_id)

        if not excluido:
            raise ValueError("Não foi possível excluir o usuário.")

        return True
