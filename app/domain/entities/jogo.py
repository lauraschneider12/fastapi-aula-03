
from dataclasses import dataclass, field
from datetime import datetime

from app.domain.entities.elenco import ElencoResumo
from app.domain.entities.cartao import Cartao


@dataclass(frozen=True)
class JogoResumo:
    local: str
    time_adversario: str
    data: datetime
    gol_local: int
    gol_visitante: int


@dataclass(frozen=True)
class GolResumo:
    id_jogador: int
    nome: str
    quantidade: int


@dataclass(frozen=True)
class Jogo:
    id: int
    local: str
    time_adversario: str
    data: datetime
    elenco_id: int
    ano_elenco: ElencoResumo
    gol_local: int
    gol_visitante: int
    gols: list[GolResumo] = field(default_factory=list)
    cartoes: list[Cartao] = field(default_factory=list)
