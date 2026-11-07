
from pydantic import BaseModel, ConfigDict


class GolCreate(BaseModel):
    id_jogo: int
    id_jogador: int


class GolUpdate(BaseModel):
    id_jogo: int
    id_jogador: int


class GolResponse(BaseModel):
    id_gol: int
    id_jogo: int
    id_jogador: int

    model_config = ConfigDict(from_attributes=True)
