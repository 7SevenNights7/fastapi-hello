"""create notes table

Revision ID: e5ba1d5180b1
Revises: 
Create Date: 2025-12-19 14:22:06.945368

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e5ba1d5180b1'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
	'notes',
	sa.Column('id', sa.Integer, primary_key=True),
	sa.Column('text', sa.Text, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('notes')
