
import asyncio
import getpass

from sqlalchemy import select

from app.infrastructure.database.session import async_session_maker
from app.infrastructure.database.models import UserModel, AdministradorModel
from app.domain.entities.user import UserRole


async def criar_admin():
    email = input("E-mail do administrador: ").strip().lower()
    nome = input("Nome do administrador: ").strip()
    senha = getpass.getpass("Senha do administrador: ")
    confirmar = getpass.getpass("Confirme a senha: ")

    if not email or not nome or not senha:
        print("Todos os campos são obrigatórios.")
        return

    if senha != confirmar:
        print("As senhas não coincidem.")
        return

    if len(senha) < 12:
        print("Use uma senha com pelo menos 12 caracteres.")
        return

    # Importação local para evitar acoplamento desnecessário
    from fastapi_users.password import PasswordHelper

    password_helper = PasswordHelper()
    senha_hash = password_helper.hash(senha)

    async with async_session_maker() as session:
        existente = await session.scalar(
            select(UserModel).where(UserModel.email == email)
        )

        if existente:
            print("Já existe um usuário com esse e-mail.")
            return

        usuario = UserModel(
            email=email,
            hashed_password=senha_hash,
            is_active=True,
            is_superuser=True,
            is_verified=True,
            role=UserRole.ADMINISTRADOR.value,
        )

        session.add(usuario)
        await session.flush()

        administrador = AdministradorModel(
            nome=nome,
            user_id=usuario.id,
        )

        session.add(administrador)
        await session.commit()

        print("Administrador inicial criado com sucesso!")



if __name__ == "__main__":
    import selectors

    asyncio.run(
        criar_admin(),
        loop_factory=lambda: asyncio.SelectorEventLoop(
            selectors.SelectSelector()
        ),
    )

