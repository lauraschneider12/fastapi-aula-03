
from dataclasses import dataclass


@dataclass(frozen=True)
class CriarElencoDTO:
    ano: int
    status: bool = True


@dataclass(frozen=True)
class AtualizarElencoDTO:
    elenco_id: int
    ano: int | None = None
    status: bool | None = None
