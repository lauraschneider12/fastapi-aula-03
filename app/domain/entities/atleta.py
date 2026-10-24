
from dataclasses import dataclass
from typing import TYPE_CHECKING
from app.domain.entities.user import UserIdentity

if TYPE_CHECKING:
    from app.domain.entities.user import UserIdentity


@dataclass(frozen=True)
class Atleta:
    id: int
    nome: str
    posicao: str
    numero: int
    status: bool
    user_identity: UserIdentity | None = None
