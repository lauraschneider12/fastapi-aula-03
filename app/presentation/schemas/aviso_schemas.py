from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CriarAvisoSchema(BaseModel):
    titulo: str = Field(min_length=1, max_length=150)
    conteudo: str = Field(min_length=1)
    elenco_id: int | None = None


class AtualizarAvisoSchema(BaseModel):
    titulo: str = Field(min_length=1, max_length=150)
    conteudo: str = Field(min_length=1)
    elenco_id: int | None = None


class AvisoRead(BaseModel):
    id: int
    titulo: str
    conteudo: str
    data_publicacao: datetime
    elenco_id: int | None
    administrador_id: int

    model_config = ConfigDict(from_attributes=True)