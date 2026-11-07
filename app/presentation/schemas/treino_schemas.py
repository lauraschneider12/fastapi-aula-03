from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TreinoCreate(BaseModel):
    data: datetime
    local: str = Field(min_length=2, max_length=200)
    descricao: str = Field(min_length=2)
    elenco_id: int = Field(gt=0)


class TreinoUpdate(BaseModel):
    data: datetime | None = None

    local: str | None = Field(
        default=None,
        min_length=2,
        max_length=200
    )

    descricao: str | None = Field(
        default=None,
        min_length=2
    )

    elenco_id: int | None = Field(
        default=None,
        gt=0
    )


class TreinoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    data: datetime
    local: str
    descricao: str
    elenco_id: int