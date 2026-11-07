
from enum import Enum
from pydantic import BaseModel, ConfigDict


class TipoCartaoSchema(str, Enum):
    AMARELO = "amarelo"
    VERMELHO = "vermelho"


class CartaoCreate(BaseModel):
    tipo: TipoCartaoSchema
    id_jogo: int
    id_jogador: int


class CartaoUpdate(BaseModel):
    tipo: TipoCartaoSchema
    id_jogo: int
    id_jogador: int


class CartaoResponse(BaseModel):
    id_cartao: int
    tipo: TipoCartaoSchema
    id_jogo: int
    id_jogador: int

    model_config = ConfigDict(from_attributes=True)
