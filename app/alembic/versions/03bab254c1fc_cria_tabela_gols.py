"""cria tabela gols

Revision ID: 03bab254c1fc
Revises: 4dc0fd1a78b0
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '03bab254c1fc'
down_revision: Union[str, Sequence[str], None] = '4dc0fd1a78b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Cria a tabela de gols."""

    op.create_table(
        'gols',
        sa.Column('id_gol', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('id_jogo', sa.Integer(), nullable=False),
        sa.Column('id_jogador', sa.Integer(), nullable=False),

        sa.ForeignKeyConstraint(
            ['id_jogo'],
            ['jogos.id'],
            ondelete='CASCADE'
        ),

        sa.PrimaryKeyConstraint('id_gol')
    )

    op.create_index(
        op.f('ix_gols_id_gol'),
        'gols',
        ['id_gol'],
        unique=False
    )


def downgrade() -> None:
    """Remove a tabela de gols."""

    op.drop_index(op.f('ix_gols_id_gol'), table_name='gols')
    op.drop_table('gols')