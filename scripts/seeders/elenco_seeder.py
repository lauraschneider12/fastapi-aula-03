
import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models import ElencoModel
from app.infrastructure.database.session import async_session_maker


ELENCOS = [
    {"ano": 2025, "status": False},
    {"ano": 2026, "status": True},
]


async def seed(session: AsyncSession) -> None:
    for dados in ELENCOS:
        resultado = await session.execute(
            select(ElencoModel).where(
                ElencoModel.ano == dados["ano"]
            )
        )
        elenco = resultado.scalar_one_or_none()

        if elenco is None:
            elenco = ElencoModel(
                ano=dados["ano"],
                status=dados["status"],
            )
            session.add(elenco)
            print(f"Elenco de {dados['ano']} criado.")
        else:
            print(f"Elenco de {dados['ano']} já existe.")


async def main() -> None:
    async with async_session_maker() as session:
        try:
            await seed(session)
            await session.commit()
            print("Seeder de elencos executada com sucesso!")
        except Exception:
            await session.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(main())
