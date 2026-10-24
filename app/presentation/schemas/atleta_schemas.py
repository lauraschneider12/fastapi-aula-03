
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AtletaCreate(BaseModel):
    nome: str = Field(min_length=2, max_length=150)
    posicao: str = Field(min_length=2, max_length=50)
    numero: int = Field(ge=1, le=99)
    email: str = Field(min_length=5, max_length=320)
    senha: str = Field(min_length=8, max_length=128)


class AtletaUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=2, max_length=150)
    posicao: str | None = Field(default=None, min_length=2, max_length=50)
    numero: int | None = Field(default=None, ge=1, le=99)
    status: bool | None = None


class AtletaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    posicao: str
    numero: int
    status: bool
    user_id: UUID
    criado_em: datetime
    alterado_em: datetime
