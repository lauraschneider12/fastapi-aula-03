from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CriarTreinoDTO:
    data: datetime
    local: str
    descricao: str
    elenco_id: int


@dataclass(frozen=True)
class AtualizarTreinoDTO:
    treino_id: int
    data: datetime | None = None
    local: str | None = None
    descricao: str | None = None
    elenco_id: int | None = None