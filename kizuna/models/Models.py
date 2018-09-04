import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

reaction_images_tags_join_table = sa.Table('reaction_images_tags_join',
                                           Base.metadata,
                                           sa.Column('reaction_image_id',
                                                     sa.Integer,
                                                     sa.ForeignKey('reaction_images.id')),
                                           sa.Column('tag_id',
                                                     sa.Integer,
                                                     sa.ForeignKey('reaction_image_tags.id')))
