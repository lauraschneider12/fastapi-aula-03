
from dataclasses import dataclass, field
from datetime import datetime

from app.domain.entities.cartao import TipoCartao


@dataclass(frozen=True)
class GolJogoDTO:
    id_jogador: int


@dataclass(frozen=True)
class CartaoJogoDTO:
    tipo: TipoCartao
    id_jogador: int


@dataclass(frozen=True)
class CriarJogoCompletoDTO:
    local: str
    time_adversario: str
    data: datetime
    elenco_id: int
    gols: list[GolJogoDTO] = field(default_factory=list)
    cartoes: list[CartaoJogoDTO] = field(default_factory=list)
