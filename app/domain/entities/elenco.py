from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from app.domain.entities.atleta_do_elenco import AtletaDoElenco

if TYPE_CHECKING:
    from app.domain.entities.atleta_do_elenco import AtletaDoElenco


@dataclass(frozen=True)
class ElencoResumo:
    ano: int


@dataclass(frozen=True)
class Elenco:
    id: int
    ano: int
    status: bool
    atletas: list[AtletaDoElenco] = field(default_factory=list)