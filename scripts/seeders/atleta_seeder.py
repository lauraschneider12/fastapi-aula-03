
import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models import UserModel, AtletaModel
from app.infrastructure.database.session import async_session_maker
from app.infrastructure.security.password_hasher import password_helper


ATLETAS = [
    {
        "nome": "João Silva",
        "posicao": "Goleiro",
        "numero": 1,
        "email": "joao@teste.com",
    },
    {
        "nome": "Pedro Santos",
        "posicao": "Defensor",
        "numero": 3,
        "email": "pedro@teste.com",
    },
    {
        "nome": "Lucas Oliveira",
        "posicao": "Meio-campo",
        "numero": 8,
        "email": "lucas@teste.com",
    },
    {
        "nome": "Gabriel Costa",
        "posicao": "Atacante",
        "numero": 9,
        "email": "gabriel@teste.com",
    },
]


async def seed(session: AsyncSession) -> None:
    for dados in ATLETAS:
        # Busca o usuário pelo e-mail
        resultado = await session.execute(
            select(UserModel).where(UserModel.email == dados["email"])
        )
        usuario = resultado.scalar_one_or_none()

        # Cria o usuário caso ainda não exista
        if usuario is None:
            usuario = UserModel(
                email=dados["email"],
                hashed_password=password_helper.hash("Atleta123"),
                is_active=True,
                is_superuser=False,
                is_verified=True,
                role="atleta",
            )
            session.add(usuario)
            await session.flush()
            print(f"Usuário criado: {dados['email']}")
        else:
            print(f"Usuário já existe: {dados['email']}")

        # Busca o perfil do atleta pelo usuário associado
        resultado = await session.execute(
            select(AtletaModel).where(
                AtletaModel.user_id == usuario.id
            )
        )
        atleta = resultado.scalar_one_or_none()

        # Cria o perfil se ainda não existir
        if atleta is None:
            atleta = AtletaModel(
                nome=dados["nome"],
                posicao=dados["posicao"],
                numero=dados["numero"],
                status=True,
                user_id=usuario.id,
            )
            session.add(atleta)
            print(f"Perfil de atleta criado: {dados['nome']}")
        else:
            print(f"Perfil já existe: {dados['nome']}")


async def main() -> None:
    async with async_session_maker() as session:
        try:
            await seed(session)
            await session.commit()
            print("Seeder de atletas executada com sucesso!")
        except Exception:
            await session.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(main())
