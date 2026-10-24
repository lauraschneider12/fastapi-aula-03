
from dataclasses import dataclass


@dataclass(frozen=True)
class CriarAtletaDTO:
    nome: str
    posicao: str
    numero: int
    email: str
    senha: str


@dataclass(frozen=True)
class AtualizarAtletaDTO:
    atleta_id: int
    nome: str | None = None
    posicao: str | None = None
    numero: int | None = None
    status: bool | None = None
