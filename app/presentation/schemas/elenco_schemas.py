
from pydantic import BaseModel, ConfigDict, Field


class ElencoCreate(BaseModel):
    ano: int = Field(ge=1900, le=2200)
    status: bool = True


class ElencoUpdate(BaseModel):
    ano: int | None = Field(default=None, ge=1900, le=2200)
    status: bool | None = None


class ElencoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ano: int
    status: bool
