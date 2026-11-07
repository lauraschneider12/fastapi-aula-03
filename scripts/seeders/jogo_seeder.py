
import asyncio
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models import ElencoModel, JogoModel
from app.infrastructure.database.session import async_session_maker


JOGOS = [
    {
        "local": "Estádio Municipal",
        "time_adversario": "União FC",
        "data": datetime(2026, 11, 15, 15, 0, tzinfo=timezone.utc),
        "placar": None,
    },
    {
        "local": "Ginásio Central",
        "time_adversario": "Atlético do Sul",
        "data": datetime(2026, 11, 22, 16, 0, tzinfo=timezone.utc),
        "placar": None,
    },
]


async def seed(session: AsyncSession) -> None:
    # Busca o elenco de 2026
    resultado = await session.execute(
        select(ElencoModel).where(ElencoModel.ano == 2026)
    )
    elenco = resultado.scalar_one_or_none()

    if elenco is None:
        raise ValueError(
            "Elenco de 2026 não encontrado. "
            "Execute primeiro o elenco_seeder."
        )

    for dados in JOGOS:
        # Evita duplicar jogos com o mesmo adversário, data e elenco
        resultado = await session.execute(
            select(JogoModel).where(
                JogoModel.elenco_id == elenco.id,
                JogoModel.time_adversario == dados["time_adversario"],
                JogoModel.data == dados["data"],
            )
        )
        jogo = resultado.scalar_one_or_none()

        if jogo is None:
            jogo = JogoModel(
                local=dados["local"],
                time_adversario=dados["time_adversario"],
                data=dados["data"],
                placar=dados["placar"],
                elenco_id=elenco.id,
            )
            session.add(jogo)
            print(
                f"Jogo contra {dados['time_adversario']} cadastrado."
            )
        else:
            print(
                f"Jogo contra {dados['time_adversario']} já existe."
            )


async def main() -> None:
    async with async_session_maker() as session:
        try:
            await seed(session)
            await session.commit()
            print("Seeder de jogos executada com sucesso!")
        except Exception:
            await session.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(main())
