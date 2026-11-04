"""initial migration

Revision ID: f8b7a9b87ae2
Revises: 
Create Date: 2026-10-16 00:25:35.211688

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8b7a9b87ae2'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('telegram_id', sa.BigInteger(), nullable=False),
    sa.Column('first_name', sa.String(length=200), nullable=False),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('language_code', sa.String(), nullable=True),
    sa.Column('is_premium', sa.Boolean(), nullable=True),
    sa.Column('is_bot', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_activity_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('telegram_id')
    )
    op.create_index(op.f('ix_users_telegram_id'), 'users', ['telegram_id'], unique=False)



def downgrade() -> None:
    op.drop_index(op.f('ix_users_telegram_id'), table_name='users')
    op.drop_table('users')
