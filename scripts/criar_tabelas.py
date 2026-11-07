
import asyncio

# Importa a conexão e a Base do SQLAlchemy
from app.infrastructure.database.session import Base, engine

# Importa os modelos para registrá-los na Base
from app.infrastructure.database import models


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()
    print("Tabelas criadas com sucesso!")


if __name__ == "__main__":
    asyncio.run(main())
