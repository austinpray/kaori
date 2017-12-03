"""add api key to users

Revision ID: 0fbc66fe58b8
Revises: 242a3ab25006
Create Date: 2017-12-03 22:49:06.036773

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fbc66fe58b8'
down_revision = '242a3ab25006'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users',
                  sa.Column('api_key', sa.String(), unique=True, index=True, nullable=False))


def downgrade():
    op.drop_column('users', 'api_key')
