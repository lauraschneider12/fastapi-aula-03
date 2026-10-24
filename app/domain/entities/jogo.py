from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING
from app.domain.entities.elenco import Elenco,ElencoResumo

if TYPE_CHECKING:
    from app.domain.entities.elenco import ElencoResumo


@dataclass(frozen=True)
class JogoResumo:
    local: str
    time_adversario: str
    data: datetime
    placar: str | None = None


@dataclass(frozen=True)
class Jogo:
    id: int
    local: str
    time_adversario: str
    data: datetime
    ano_elenco: ElencoResumo
    placar: str | None = None