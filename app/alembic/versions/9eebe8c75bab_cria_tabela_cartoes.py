"""cria tabela cartoes

Revision ID: 9eebe8c75bab
Revises: 03bab254c1fc
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '9eebe8c75bab'
down_revision: Union[str, Sequence[str], None] = '03bab254c1fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Cria a tabela de cartões."""

    op.create_table(
        'cartoes',

        sa.Column(
            'id_cartao',
            sa.Integer(),
            autoincrement=True,
            nullable=False
        ),

        sa.Column(
            'tipo',
            sa.String(length=50),
            nullable=False
        ),

        sa.Column(
            'id_jogo',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'id_jogador',
            sa.Integer(),
            nullable=False
        ),

        sa.ForeignKeyConstraint(
            ['id_jogo'],
            ['jogos.id'],
            ondelete='CASCADE'
        ),

        sa.ForeignKeyConstraint(
            ['id_jogador'],
            ['atletas.id'],
            ondelete='CASCADE'
        ),

        sa.PrimaryKeyConstraint('id_cartao')
    )

    op.create_index(
        op.f('ix_cartoes_id_cartao'),
        'cartoes',
        ['id_cartao'],
        unique=False
    )


def downgrade() -> None:
    """Remove a tabela de cartões."""

    op.drop_index(
        op.f('ix_cartoes_id_cartao'),
        table_name='cartoes'
    )

    op.drop_table('cartoes')