
import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models import (
    AtletaModel,
    ElencoModel,
    AtletaElencoModel,
)
from app.infrastructure.database.session import async_session_maker


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

    # Busca todos os atletas ativos
    resultado = await session.execute(
        select(AtletaModel).where(AtletaModel.status.is_(True))
    )
    atletas = resultado.scalars().all()

    if not atletas:
        print("Nenhum atleta ativo encontrado.")
        return

    for atleta in atletas:
        # Verifica se a associação já existe
        resultado = await session.execute(
            select(AtletaElencoModel).where(
                AtletaElencoModel.atleta_id == atleta.id,
                AtletaElencoModel.elenco_id == elenco.id,
            )
        )
        associacao = resultado.scalar_one_or_none()

        if associacao is None:
            associacao = AtletaElencoModel(
                atleta_id=atleta.id,
                elenco_id=elenco.id,
            )
            session.add(associacao)
            print(
                f"Atleta {atleta.nome} associado ao elenco de 2026."
            )
        else:
            print(
                f"Atleta {atleta.nome} já está no elenco de 2026."
            )


async def main() -> None:
    async with async_session_maker() as session:
        try:
            await seed(session)
            await session.commit()
            print("Seeder de associações executada com sucesso!")
        except Exception:
            await session.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(main())
