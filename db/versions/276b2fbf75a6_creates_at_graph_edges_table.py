"""creates at_graph_edges table

Revision ID: 276b2fbf75a6
Revises: 380c385b82a6
Create Date: 2017-11-29 06:52:16.116826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '276b2fbf75a6'
down_revision = '380c385b82a6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'at_graph_edges',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('head_user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('tail_user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('weight', sa.Integer, nullable=False)
    )


def downgrade():
    op.drop_table('at_graph_edges')
