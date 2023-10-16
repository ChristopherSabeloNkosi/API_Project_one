"""add column to posts

Revision ID: 50a2b48350df
Revises: 40fc24bb5529
Create Date: 2023-10-12 23:18:30.147444

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50a2b48350df'
down_revision: Union[str, None] = '40fc24bb5529'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('Posts', 'content')
    pass
