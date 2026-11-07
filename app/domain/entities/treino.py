from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Treino:
    id: int
    data: datetime
    local: str
    descricao: str
    elenco_id: int