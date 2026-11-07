
import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models import UserModel, AdministradorModel
from app.infrastructure.database.session import async_session_maker
from app.infrastructure.security.password_hasher import password_helper


async def seed(session: AsyncSession) -> None:
    email = "admin@teste.com"

    # Verifica se o usuário já existe
    resultado = await session.execute(
        select(UserModel).where(UserModel.email == email)
    )
    usuario = resultado.scalar_one_or_none()

    if usuario is None:
        usuario = UserModel(
            email=email,
            hashed_password=password_helper.hash("Admin123"),
            is_active=True,
            is_superuser=True,
            is_verified=True,
            role="administrador",
        )
        session.add(usuario)
        await session.flush()
        print(f"Usuário administrador criado: {email}")
    else:
        print(f"Usuário já existe: {email}")

    # Cria o perfil de administrador, se ainda não existir
    resultado = await session.execute(
        select(AdministradorModel).where(
            AdministradorModel.user_id == usuario.id
        )
    )
    administrador = resultado.scalar_one_or_none()

    if administrador is None:
        administrador = AdministradorModel(
            nome="Administrador de Teste",
            user_id=usuario.id,
        )
        session.add(administrador)
        print("Perfil de administrador criado.")
    else:
        print("Perfil de administrador já existe.")


async def main() -> None:
    async with async_session_maker() as session:
        try:
            await seed(session)
            await session.commit()
            print("Seeder de usuário executada com sucesso!")
        except Exception:
            await session.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(main())
