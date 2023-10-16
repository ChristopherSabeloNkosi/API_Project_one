"""add foreign_key to posts table

Revision ID: 496bb3049831
Revises: bb989dd227a3
Create Date: 2023-10-12 23:40:34.965681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '496bb3049831'
down_revision: Union[str, None] = 'bb989dd227a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Posts', sa.Column('owner_id', sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fkey', source_table='Posts',referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fkey', table_name='Posts')
    op.drop_column('Posts', 'owner_id')

    pass
