"""cria tabela presencas

Revision ID: fc74a26f747a
Revises: 22844c734221
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "fc74a26f747a"
down_revision: Union[str, Sequence[str], None] = "22844c734221"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "presencas",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("atleta_id", sa.Integer(), nullable=False),
        sa.Column("treino_id", sa.Integer(), nullable=False),
        sa.Column("confirmacao", sa.Boolean(), nullable=True),
        sa.Column("presente", sa.Boolean(), nullable=True),
        sa.Column("confirmado_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("registrado_em", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["atleta_id"],
            ["atletas.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["treino_id"],
            ["treinos.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "atleta_id",
            "treino_id",
            name="uq_presenca_atleta_treino",
        ),
    )

    op.create_index(
        op.f("ix_presencas_id"),
        "presencas",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_presencas_id"), table_name="presencas")
    op.drop_table("presencas")