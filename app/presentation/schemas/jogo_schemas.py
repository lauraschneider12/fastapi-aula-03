
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domain.entities.cartao import TipoCartao


class GolJogoCreate(BaseModel):
    id_jogador: int = Field(gt=0)


class CartaoJogoCreate(BaseModel):
    tipo: TipoCartao
    id_jogador: int = Field(gt=0)


class JogoCreate(BaseModel):
    local: str = Field(min_length=2, max_length=200)
    time_adversario: str = Field(min_length=2, max_length=150)
    data: datetime
    elenco_id: int = Field(gt=0)

    gols: list[GolJogoCreate] = Field(default_factory=list)
    cartoes: list[CartaoJogoCreate] = Field(default_factory=list)


class JogoUpdate(BaseModel):
    local: str | None = Field(
        default=None,
        min_length=2,
        max_length=200
    )
    time_adversario: str | None = Field(
        default=None,
        min_length=2,
        max_length=150
    )
    data: datetime | None = None
    elenco_id: int | None = Field(default=None, gt=0)

    gols: list[GolJogoCreate] | None = None
    cartoes: list[CartaoJogoCreate] | None = None


class GolJogoRead(BaseModel):
    id_jogador: int
    nome: str
    quantidade: int


class CartaoJogoRead(BaseModel):
    id_cartao: int
    tipo: TipoCartao
    id_jogador: int


class JogoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    local: str
    time_adversario: str
    data: datetime
    elenco_id: int
    gol_local: int
    gol_visitante: int

    gols: list[GolJogoRead] = Field(default_factory=list)
    cartoes: list[CartaoJogoRead] = Field(default_factory=list)
