from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.session import Base


class GolModel(Base):
    __tablename__ = "gols"

    id_gol: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    id_jogo: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("jogos.id", ondelete="CASCADE"),
        nullable=False,
    )

    id_jogador: Mapped[int] = mapped_column(
    Integer,
    nullable=False,
    )