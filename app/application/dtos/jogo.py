from dataclasses import dataclass
from datetime import datetime

from app.application.dtos.gol import CriarGolDTO
from app.application.dtos.cartao import CriarCartaoDTO


@dataclass(frozen=True)
class CriarJogoDTO:
    local: str
    time_adversario: str
    data: datetime
    elenco_id: int
    gol_local: int = 0
    gol_visitante: int = 0


@dataclass(frozen=True)
class AtualizarJogoDTO:
    jogo_id: int
    local: str | None = None
    time_adversario: str | None = None
    data: datetime | None = None
    elenco_id: int | None = None
    gols: list[CriarGolDTO] | None = None
    cartoes: list[CriarCartaoDTO] | None = None