"""cria tabela avisos

Revision ID: 61b0f9b39f0b
Revises: fc74a26f747a
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "61b0f9b39f0b"
down_revision: Union[str, Sequence[str], None] = "fc74a26f747a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "avisos",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("titulo", sa.String(length=150), nullable=False),
        sa.Column("conteudo", sa.Text(), nullable=False),
        sa.Column("data_publicacao", sa.DateTime(timezone=True), nullable=False),
        sa.Column("elenco_id", sa.Integer(), nullable=True),
        sa.Column("administrador_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["elenco_id"],
            ["elencos.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["administrador_id"],
            ["administradores.id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_avisos_id"),
        "avisos",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_avisos_id"), table_name="avisos")
    op.drop_table("avisos")