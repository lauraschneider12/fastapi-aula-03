from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.entities.user import UserIdentity

@dataclass(frozen=True)
class Administrador:
    id: int
    nome: str
    user_identity: "UserIdentity"
