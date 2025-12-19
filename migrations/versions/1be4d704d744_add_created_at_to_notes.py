"""add created_at to notes

Revision ID: 1be4d704d744
Revises: e5ba1d5180b1
Create Date: 2025-12-19 14:48:02.930822

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1be4d704d744'
down_revision: Union[str, Sequence[str], None] = 'e5ba1d5180b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     op.add_column(
        'notes',
        sa.Column(
            'created_at',
            sa.DateTime(),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column('notes', 'created_at')
