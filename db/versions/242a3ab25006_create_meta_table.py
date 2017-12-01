"""create meta table

Revision ID: 242a3ab25006
Revises: 276b2fbf75a6
Create Date: 2017-12-01 04:58:09.072673

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '242a3ab25006'
down_revision = '276b2fbf75a6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'meta',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('key', sa.String, index=True, unique=True),
        sa.Column('value', sa.String),
    )


def downgrade():
    op.drop_table('meta')
