"""adds kkreds transactions

Revision ID: 8c97dd056cea
Revises: 10e4ec33e1fb
Create Date: 2017-12-18 14:20:55.175749

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c97dd056cea'
down_revision = '10e4ec33e1fb'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'kkreds_transactions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('from_user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('to_user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('amount', sa.DECIMAL, nullable=False),
        sa.Column('created_at', sa.DateTime, default=sa.func.current_timestamp()),
        sa.Column('is_mined', sa.Boolean, default=False)
    )


def downgrade():
    op.drop_table('kkreds_transactions')
