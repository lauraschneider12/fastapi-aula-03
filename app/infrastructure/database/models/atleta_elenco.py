from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.session import Base
from app.infrastructure.database.models.atleta import AtletaModel


class AtletaElencoModel(Base):
    __tablename__ = "atletas_elencos"

    atleta_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("atletas.id", ondelete="CASCADE"),
        primary_key=True,
    )

    elenco_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("elencos.id", ondelete="CASCADE"),
        primary_key=True,
    )

    atleta: Mapped["AtletaModel"] = relationship(
        back_populates="elencos",
    )

    elenco: Mapped["ElencoModel"] = relationship(
        back_populates="atletas",
    )