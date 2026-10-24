
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CriarUserDTO:
    email: str
    senha: str
    role: str = "atleta"


@dataclass(frozen=True)
class AtualizarUserDTO:
    user_id: UUID
    email: str | None = None
    role: str | None = None
