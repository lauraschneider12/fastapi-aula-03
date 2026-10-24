
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class JogoCreate(BaseModel):
    local: str = Field(min_length=2, max_length=200)
    time_adversario: str = Field(min_length=2, max_length=150)
    data: datetime
    placar: str | None = Field(default=None, max_length=30)
    elenco_id: int = Field(gt=0)


class JogoUpdate(BaseModel):
    local: str | None = Field(default=None, min_length=2, max_length=200)
    time_adversario: str | None = Field(default=None, min_length=2, max_length=150)
    data: datetime | None = None
    placar: str | None = Field(default=None, max_length=30)
    elenco_id: int | None = Field(default=None, gt=0)


class JogoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    local: str
    time_adversario: str
    data: datetime
    placar: str | None
    elenco_id: int
