
from dataclasses import dataclass
from typing import TYPE_CHECKING
from app.domain.entities.atleta import Atleta

if TYPE_CHECKING:
    from app.domain.entities.atleta import Atleta


@dataclass(frozen=True)
class AtletaDoElenco:
    atleta_id: int
    elenco_id: int
    atleta: Atleta | None = None
