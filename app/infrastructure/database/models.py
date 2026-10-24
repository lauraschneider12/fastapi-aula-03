
import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UUID,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.entities.user import UserRole
from app.infrastructure.database.session import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    email: Mapped[str] = mapped_column(
        String(320),
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(1024),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        String(20),
        nullable=False,
        default=UserRole.ATLETA,
    )

    atleta: Mapped["AtletaModel | None"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )

    administrador: Mapped["AdministradorModel | None"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )


class AtletaModel(Base):
    __tablename__ = "atletas"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    nome: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    posicao: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    numero: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    status: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    alterado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user: Mapped["UserModel"] = relationship(
        back_populates="atleta",
    )

    elencos: Mapped[list["AtletaElencoModel"]] = relationship(
        back_populates="atleta",
        cascade="all, delete-orphan",
    )


class AdministradorModel(Base):
    __tablename__ = "administradores"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    nome: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    user: Mapped["UserModel"] = relationship(
        back_populates="administrador",
    )


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

    placar: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    elenco_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("elencos.id", ondelete="RESTRICT"),
        nullable=False,
    )

    elenco: Mapped["ElencoModel"] = relationship(
        back_populates="jogos",
    )
