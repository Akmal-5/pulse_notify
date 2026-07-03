"""clean_start

Revision ID: a36a89c474da
Revises: 
Create Date: 2026-07-03 17:09:17.129934

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a36a89c474da'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=60), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('telegram_chat_id', sa.String(length=80), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('userteste',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=False),
    sa.Column('code', sa.String(length=20), nullable=False),
    sa.Column('attempts', sa.Integer(), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('target',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=200), nullable=False),
    sa.Column('http_method', sa.String(length=10), nullable=False),
    sa.Column('interval_seconds', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('checklog',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('target_id', sa.Integer(), nullable=False),
    sa.Column('status_code', sa.Integer(), nullable=True),
    sa.Column('is_up', sa.Boolean(), nullable=False),
    sa.Column('error_message', sa.Text(), nullable=False),
    sa.Column('checked_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['target_id'], ['target.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_checklog_checked_at'), 'checklog', ['checked_at'], unique=False)
  

def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(op.f('ix_checklog_checked_at'), table_name='checklog')
    op.drop_table('checklog')
    op.drop_table('target')
    op.drop_table('userteste')
    op.drop_table('users')