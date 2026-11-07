from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AtualizarConfirmacaoSchema(BaseModel):
    treino_id: int
    confirmacao: bool


class AtualizarPresenteSchema(BaseModel):
    atleta_id: int
    treino_id: int
    presente: bool


class PresencaRead(BaseModel):
    id: int
    atleta_id: int
    treino_id: int
    confirmacao: bool | None
    presente: bool | None
    confirmado_em: datetime | None
    registrado_em: datetime | None

    model_config = ConfigDict(from_attributes=True)