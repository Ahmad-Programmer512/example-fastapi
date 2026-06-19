"""add content column to posts table

Revision ID: e608e3223569
Revises: 821471477398
Create Date: 2026-06-17 20:40:33.516505

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e608e3223569'
down_revision: Union[str, Sequence[str], None] = '821471477398'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
