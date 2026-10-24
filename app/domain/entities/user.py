import enum
from dataclasses import dataclass
from uuid import UUID


class UserRole(str, enum.Enum):
    ATLETA = "atleta"
    ADMINISTRADOR = "administrador"


@dataclass(frozen=True)
class UserIdentity:
    id: UUID
    email: str
    role: UserRole