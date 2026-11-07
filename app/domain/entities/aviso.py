from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Aviso:
    id: int
    titulo: str
    conteudo: str
    data_publicacao: datetime
    elenco_id: int | None
    administrador_id: int