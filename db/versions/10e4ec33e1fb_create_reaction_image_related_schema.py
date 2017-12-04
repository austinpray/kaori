"""create reaction image related schema

Revision ID: 10e4ec33e1fb
Revises: 0fbc66fe58b8
Create Date: 2017-12-05 02:28:00.589532

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10e4ec33e1fb'
down_revision = '0fbc66fe58b8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('reaction_images',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('url', sa.String, index=True, unique=True),
                    sa.Column('name', sa.String),
                    sa.Column('type', sa.String),
                    sa.Column('description', sa.Text),
                    sa.Column('created_at',
                              sa.DateTime,
                              default=sa.func.current_timestamp()),
                    sa.Column('updated_at',
                              sa.DateTime,
                              default=sa.func.current_timestamp(),
                              onupdate=sa.func.current_timestamp()))

    op.create_table('reaction_image_tags',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('name', sa.String, index=True, unique=True),
                    sa.Column('description', sa.Text),
                    sa.Column('created_at', sa.DateTime, default=sa.func.current_timestamp()),
                    sa.Column('updated_at',
                              sa.DateTime,
                              default=sa.func.current_timestamp(),
                              onupdate=sa.func.current_timestamp()))

    op.create_table('reaction_images_tags_join',
                    sa.Column('reaction_image_id', sa.Integer, sa.ForeignKey('reaction_images.id', ondelete='CASCADE')),
                    sa.Column('tag_id', sa.Integer, sa.ForeignKey('reaction_image_tags.id', ondelete='CASCADE')))


def downgrade():
    op.drop_table('reaction_images_tags_join')
    op.drop_table('reaction_images')
    op.drop_table('reaction_image_tags')
