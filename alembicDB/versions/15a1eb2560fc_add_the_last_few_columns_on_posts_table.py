"""add the last few columns on posts table

Revision ID: 15a1eb2560fc
Revises: 496bb3049831
Create Date: 2023-10-12 23:56:55.039298

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15a1eb2560fc'
down_revision: Union[str, None] = '496bb3049831'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Posts',
                  sa.Column('published', sa.Boolean(), nullable=False,server_default='TRUE'),)
    op.add_column('Posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                      nullable=False,server_default=sa.text('NOW()')),)
    
    pass


def downgrade() -> None:
    op.drop_column('Posts', 'published')
    op.drop_column('Posts', 'created_at')
    pass
