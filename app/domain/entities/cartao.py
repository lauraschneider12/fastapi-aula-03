from dataclasses import dataclass
from enum import Enum


class TipoCartao(str, Enum):
    AMARELO = "amarelo"
    VERMELHO = "vermelho"


@dataclass(frozen=True)
class Cartao:
    id_cartao: int
    tipo: TipoCartao
    id_jogo: int
    id_jogador: int