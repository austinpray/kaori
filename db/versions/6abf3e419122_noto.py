"""noto

Revision ID: 6abf3e419122
Revises: facd92ba87b7
Create Date: 2018-09-01 13:41:08.898839

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = '6abf3e419122'
down_revision = 'facd92ba87b7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'languages',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('bcp47', sa.String, nullable=False)
    )
    languages = table(
        'languages',
        sa.Column('name', sa.String),
        sa.Column('bcp47', sa.String)
    )
    op.bulk_insert(
        languages,
        [
            {'name': 'English', 'bcp47': 'en'},
            {'name': 'Japanese', 'bcp47': 'ja'},
        ]
    )
    op.create_table(
        'slack_teams',
        sa.Column('id', sa.String, primary_key=True),
        sa.Column('name', sa.String)
    )

    op.create_table(
        'slack_messages',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('slack_team_id', sa.String, sa.ForeignKey('slack_teams.id')),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('channel', sa.String, nullable=False),
        sa.Column('ts', sa.String, nullable=False),
        sa.Column('text', sa.Text)

    )
    op.create_table(
        'noto_notes',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('parent_id', sa.BigInteger),
        sa.Column('language_id', sa.Integer, sa.ForeignKey('languages.id')),
        sa.Column('slack_message_id', sa.BigInteger, sa.ForeignKey('slack_messages.id')),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('text', sa.Text),
        sa.Column('description', sa.Text),
        sa.Column('deleted', sa.Boolean, default=False),
        sa.Column('created_at', sa.DateTime, default=sa.func.current_timestamp()),
    )


def downgrade():
    op.drop_table('noto_notes')
    op.drop_table('slack_messages')
    op.drop_table('slack_teams')
    op.drop_table('languages')
