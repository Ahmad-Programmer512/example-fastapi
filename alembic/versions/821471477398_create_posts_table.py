"""create posts table

Revision ID: 821471477398
Revises: 
Create Date: 2026-06-17 17:11:52.309547

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '821471477398'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=True, primary_key=True),
                    sa.Column('title', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_table('posts')
