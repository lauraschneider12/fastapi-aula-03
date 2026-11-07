from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.session import Base

class AvisoModel(Base):
    __tablename__ = "avisos"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    titulo: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    conteudo: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    data_publicacao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    elenco_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("elencos.id", ondelete="CASCADE"),
        nullable=True,
    )

    administrador_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("administradores.id", ondelete="RESTRICT"),
        nullable=False,
    )

    elenco: Mapped["ElencoModel | None"] = relationship()
    administrador: Mapped["AdministradorModel"] = relationship()