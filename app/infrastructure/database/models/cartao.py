from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.session import Base


class CartaoModel(Base):
    __tablename__ = "cartoes"

    id_cartao: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    tipo: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    id_jogo: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("jogos.id", ondelete="CASCADE"),
        nullable=False,
    )

    id_jogador: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("atletas.id", ondelete="CASCADE"),
        nullable=False,
    )