"""atualiza estrutura jogos

Revision ID: 4dc0fd1a78b0
Revises: 4a1c3149665e
Create Date: 2026-10-30
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Identificação da migration
revision: str = '4dc0fd1a78b0'
down_revision: Union[str, Sequence[str], None] = '4a1c3149665e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Atualiza a estrutura da tabela jogos."""

    # Remove a coluna antiga de placar
    op.drop_column('jogos', 'placar')

    # Adiciona os gols do time local
    op.add_column(
        'jogos',
        sa.Column(
            'gol_local',
            sa.Integer(),
            nullable=False,
            server_default='0'
        )
    )

    # Adiciona os gols do time visitante
    op.add_column(
        'jogos',
        sa.Column(
            'gol_visitante',
            sa.Integer(),
            nullable=False,
            server_default='0'
        )
    )


def downgrade() -> None:
    """Reverte a alteração da tabela jogos."""

    op.drop_column('jogos', 'gol_visitante')
    op.drop_column('jogos', 'gol_local')

    op.add_column(
        'jogos',
        sa.Column(
            'placar',
            sa.String(length=30),
            nullable=True
        )
    )