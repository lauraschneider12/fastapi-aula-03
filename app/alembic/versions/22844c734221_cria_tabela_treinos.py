"""cria tabela treinos

Revision ID: 22844c734221
Revises: 9eebe8c75bab
Create Date: 2026-11-05 22:31:02.745057
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "22844c734221"
down_revision: Union[str, Sequence[str], None] = "9eebe8c75bab"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "treinos",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("data", sa.DateTime(timezone=True), nullable=False),
        sa.Column("local", sa.String(length=200), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=False),
        sa.Column("elenco_id", sa.Integer(), nullable=False),
        sa.Column("criado_em", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["elenco_id"],
            ["elencos.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_treinos_id"),
        "treinos",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_treinos_id"), table_name="treinos")
    op.drop_table("treinos")