
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Sessão do banco
from app.infrastructure.database.session import get_db

# Implementações dos repositórios
from app.infrastructure.repositories.jogo_repository_impl import JogoRepositoryImpl
from app.infrastructure.repositories.elenco_repository_impl import ElencoRepositoryImpl
from app.infrastructure.repositories.atleta_repository_impl import AtletaRepositoryImpl
from app.infrastructure.repositories.gol_repository_impl import GolRepositoryImpl
from app.infrastructure.repositories.cartao_repository_impl import CartaoRepositoryImpl
from app.infrastructure.repositories.treino_repository_impl import TreinoRepositoryImpl
from app.infrastructure.repositories.presenca_repository_impl import PresencaRepositoryImpl
from app.infrastructure.repositories.aviso_repository_impl import AvisoRepositoryImpl
# Casos de uso
from app.application.use_cases.jogo import JogoUseCases
from app.application.use_cases.gol import GolUseCases
from app.application.use_cases.cartao import CartaoUseCases
from app.application.use_cases.jogo_completo import JogoCompletoUseCase
from app.application.use_cases.treino import TreinoUseCases
from app.application.use_cases.presenca import PresencaUseCases
from app.application.use_cases.aviso import AvisoUseCases



# Dependência de jogos
def get_jogo_use_cases(
    session: AsyncSession = Depends(get_db),
) -> JogoUseCases:

    return JogoUseCases(
        jogo_repository=JogoRepositoryImpl(session),
        elenco_repository=ElencoRepositoryImpl(session),
        gol_repository=GolRepositoryImpl(session),
        cartao_repository=CartaoRepositoryImpl(session),
        atleta_repository=AtletaRepositoryImpl(session),
    )



# Dependência de gols
def get_gol_use_cases(
    session: AsyncSession = Depends(get_db),
) -> GolUseCases:

    return GolUseCases(
        gol_repository=GolRepositoryImpl(session),
        jogo_repository=JogoRepositoryImpl(session),
        atleta_repository=AtletaRepositoryImpl(session),
    )


# Dependência de cartões
def get_cartao_use_cases(
    session: AsyncSession = Depends(get_db),
) -> CartaoUseCases:

    return CartaoUseCases(
        cartao_repository=CartaoRepositoryImpl(session),
        jogo_repository=JogoRepositoryImpl(session),
        atleta_repository=AtletaRepositoryImpl(session),
    )


# Dependência de jogo completo
def get_jogo_completo_use_case(
    session: AsyncSession = Depends(get_db),
) -> JogoCompletoUseCase:

    return JogoCompletoUseCase(
        jogo_repository=JogoRepositoryImpl(session),
        elenco_repository=ElencoRepositoryImpl(session),
        gol_repository=GolRepositoryImpl(session),
        cartao_repository=CartaoRepositoryImpl(session),
        atleta_repository=AtletaRepositoryImpl(session),
    )

# Dependência de treinos
def get_treino_use_cases(
    session: AsyncSession = Depends(get_db),
) -> TreinoUseCases:

    return TreinoUseCases(
        treino_repository=TreinoRepositoryImpl(session),
        elenco_repository=ElencoRepositoryImpl(session),
    )

def get_presenca_use_cases(
    session: AsyncSession = Depends(get_db),
) -> PresencaUseCases:

    return PresencaUseCases(
        presenca_repository=PresencaRepositoryImpl(session),
        atleta_repository=AtletaRepositoryImpl(session),
        treino_repository=TreinoRepositoryImpl(session),
    )
# Dependência de avisos
def get_aviso_use_cases(
    session: AsyncSession = Depends(get_db),
) -> AvisoUseCases:

    return AvisoUseCases(
        aviso_repository=AvisoRepositoryImpl(session),
        session=session,
    )