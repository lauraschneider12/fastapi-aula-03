
import asyncio

from app.infrastructure.database.session import async_session_maker

from scripts.seeders.user_seeder import seed as seed_users
from scripts.seeders.atleta_seeder import seed as seed_atletas
from scripts.seeders.elenco_seeder import seed as seed_elencos
from scripts.seeders.atleta_elenco_seeder import seed as seed_atleta_elenco
from scripts.seeders.jogo_seeder import seed as seed_jogos


async def main() -> None:
    async with async_session_maker() as session:
        try:
            print("\n=== 1. Usuário administrador ===")
            await seed_users(session)

            print("\n=== 2. Atletas ===")
            await seed_atletas(session)

            print("\n=== 3. Elencos ===")
            await seed_elencos(session)

            print("\n=== 4. Associações atleta-elenco ===")
            await seed_atleta_elenco(session)

            print("\n=== 5. Jogos ===")
            await seed_jogos(session)

            await session.commit()
            print("\nTodas as seeders foram executadas com sucesso!")

        except Exception:
            await session.rollback()
            print("\nErro ao executar as seeders. Alterações desfeitas.")
            raise


if __name__ == "__main__":
    asyncio.run(main())
