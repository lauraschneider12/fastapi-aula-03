
from dataclasses import dataclass


@dataclass(frozen=True)
class CriarGolDTO:
    id_jogo: int
    id_jogador: int


@dataclass(frozen=True)
class AtualizarGolDTO:
    id_gol: int
    id_jogo: int
    id_jogador: int
