
from dataclasses import dataclass

from app.domain.entities.cartao import TipoCartao


@dataclass(frozen=True)
class CriarCartaoDTO:
    tipo: TipoCartao
    id_jogo: int
    id_jogador: int


@dataclass(frozen=True)
class AtualizarCartaoDTO:
    id_cartao: int
    tipo: TipoCartao
    id_jogo: int
    id_jogador: int
