from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Presenca:
    id: int
    atleta_id: int
    treino_id: int
    confirmacao: bool | None = None
    presente: bool | None = None
    confirmado_em: datetime | None = None
    registrado_em: datetime | None = None