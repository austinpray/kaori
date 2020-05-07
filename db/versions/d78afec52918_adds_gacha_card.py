"""adds gacha card

Revision ID: d78afec52918
Revises: facd92ba87b7
Create Date: 2020-04-21 04:52:41.180265

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'd78afec52918'
down_revision = 'facd92ba87b7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'images',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created_at', sa.DateTime, default=sa.func.current_timestamp()),

        sa.Column('url', sa.Text, nullable=False),
        sa.Column('slack_file_id', sa.Text),

        sa.Column('owner', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
    )

    op.create_table(
        'cards',
        sa.Column('id', sa.Integer, primary_key=True),

        sa.Column('created_at', sa.DateTime, default=sa.func.current_timestamp()),

        sa.Column('name', sa.UnicodeText, nullable=False, unique=True),
        sa.Column('slug', sa.UnicodeText, nullable=False, unique=True),

        # creation related
        sa.Column('owner', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('published', sa.Boolean, nullable=False, default=False),
        sa.Column('creation_thread_channel', sa.Text, nullable=False),
        sa.Column('creation_thread_ts', sa.Text, nullable=False, unique=True),
        sa.Column('draft_message_ts', sa.Text),
        sa.Column('creation_cursor', sa.Text, default='blank'),

        sa.Column('image_id', sa.Integer, sa.ForeignKey('images.id')),

        sa.Column('description', sa.UnicodeText),

        sa.Column('rarity', sa.Integer),

        sa.Column('hit_points', sa.Integer),

        sa.Column('stupid', sa.Integer),
        sa.Column('baby', sa.Integer),
        sa.Column('cursed', sa.Integer),
        sa.Column('horny', sa.Integer),
        sa.Column('clown', sa.Integer),
        sa.Column('feral', sa.Integer),

    )


def downgrade():
    op.drop_table('cards')
    op.drop_table('images')
