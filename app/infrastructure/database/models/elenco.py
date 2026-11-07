from sqlalchemy import Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.infrastructure.database.session import Base
from app.infrastructure.database.models.atleta_elenco import AtletaElencoModel


class ElencoModel(Base):
    __tablename__ = "elencos"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    ano: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        unique=True,
    )

    status: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    atletas: Mapped[list["AtletaElencoModel"]] = relationship(
        back_populates="elenco",
        cascade="all, delete-orphan",
    )

    jogos: Mapped[list["JogoModel"]] = relationship(
        back_populates="elenco",
    )
    treinos: Mapped[list["TreinoModel"]] = relationship(
    "TreinoModel",
    back_populates="elenco",
)