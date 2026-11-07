from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.session import Base


class PresencaModel(Base):
    __tablename__ = "presencas"

    __table_args__ = (
        UniqueConstraint(
            "atleta_id",
            "treino_id",
            name="uq_presenca_atleta_treino",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    atleta_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("atletas.id", ondelete="CASCADE"),
        nullable=False,
    )

    treino_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("treinos.id", ondelete="CASCADE"),
        nullable=False,
    )

    # None = ainda não respondeu; True = confirmou; False = não confirmou.
    confirmacao: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
        default=None,
    )

    # None = comissão ainda não registrou; True = presente; False = ausente.
    presente: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
        default=None,
    )

    confirmado_em: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    registrado_em: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    atleta: Mapped["AtletaModel"] = relationship()
    treino: Mapped["TreinoModel"] = relationship()