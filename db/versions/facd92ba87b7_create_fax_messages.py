"""create_fax_messages

Revision ID: facd92ba87b7
Revises: 8c97dd056cea
Create Date: 2018-02-17 22:09:33.844242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'facd92ba87b7'
down_revision = '8c97dd056cea'
branch_labels = None
depends_on = None

FAX_MESSAGES = 'fax_messages'

def upgrade():
    op.create_table(
        FAX_MESSAGES,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('trigger_id', sa.String, index=True, unique=True),
        sa.Column('user_name', sa.String),
        sa.Column('user_id', sa.String),
        sa.Column('team_id', sa.String),
        sa.Column('text', sa.Text),
        sa.Column('created_at', sa.DateTime, default=sa.func.current_timestamp()),
        sa.Column('printed_at', sa.DateTime)
    )


def downgrade():
    op.drop_table(FAX_MESSAGES)
