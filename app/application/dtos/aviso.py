from dataclasses import dataclass


@dataclass
class CriarAvisoDTO:
    titulo: str
    conteudo: str
    elenco_id: int | None = None


@dataclass
class AtualizarAvisoDTO:
    aviso_id: int
    titulo: str
    conteudo: str
    elenco_id: int | None = None