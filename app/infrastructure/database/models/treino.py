from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.session import Base


class TreinoModel(Base):
    __tablename__ = "treinos"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    data: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    local: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    descricao: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    elenco_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("elencos.id", ondelete="CASCADE"),
        nullable=False,
    )

    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    elenco: Mapped["ElencoModel"] = relationship(
        "ElencoModel",
        back_populates="treinos",
    )