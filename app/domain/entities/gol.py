from dataclasses import dataclass


@dataclass(frozen=True)
class Gol:
    id_gol: int
    id_jogo: int
    id_jogador: int