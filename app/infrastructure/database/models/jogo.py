from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.session import Base


class JogoModel(Base):
    __tablename__ = "jogos"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    local: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    time_adversario: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    data: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    gol_local: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    gol_visitante: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    elenco_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("elencos.id", ondelete="RESTRICT"),
        nullable=False,
    )

    elenco: Mapped["ElencoModel"] = relationship(
        back_populates="jogos",
    )