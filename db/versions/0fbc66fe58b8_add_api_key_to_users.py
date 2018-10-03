"""add api key to users

Revision ID: 0fbc66fe58b8
Revises: 242a3ab25006
Create Date: 2017-12-03 22:49:06.036773

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import select


from ...src.support.models.User import user_generate_api_key

# revision identifiers, used by Alembic.
revision = '0fbc66fe58b8'
down_revision = '242a3ab25006'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('api_key', sa.String()))
    conn = op.get_bind().connect()
    users = sa.sql.table('users',
                         sa.Column('id', sa.Integer),
                         sa.Column('api_key', sa.String))

    users_res = conn.execute(select([users.c.id])).fetchall()

    for user in users_res:
        conn.execute(users.update().where(users.c.id == user[users.c.id]).values(api_key=user_generate_api_key()))

    op.alter_column('users', 'api_key', nullable=False)
    op.create_index('ix_api_key', 'users', ['api_key'], unique=True)


def downgrade():
    op.drop_column('users', 'api_key')
