
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CriarJogoDTO:
    local: str
    time_adversario: str
    data: datetime
    elenco_id: int
    placar: str | None = None


@dataclass(frozen=True)
class AtualizarJogoDTO:
    jogo_id: int
    local: str | None = None
    time_adversario: str | None = None
    data: datetime | None = None
    elenco_id: int | None = None
    placar: str | None = None
