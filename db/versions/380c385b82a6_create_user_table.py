"""create user table

Revision ID: 380c385b82a6
Revises:
Create Date: 2017-11-29 06:35:00.723089

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '380c385b82a6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('slack_id', sa.String, index=True, unique=True),
    )


def downgrade():
    op.drop_table('users')
