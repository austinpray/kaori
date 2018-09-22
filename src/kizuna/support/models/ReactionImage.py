from sqlalchemy import Column, Integer, String, DateTime, func, Text
from sqlalchemy.orm import relationship

from . import Base, reaction_images_tags_join_table


class ReactionImage(Base):
    __tablename__ = 'reaction_images'

    id = Column(Integer, primary_key=True)
    url = Column(String, index=True, unique=True)
    name = Column(String)
    type = Column(String)
    description = Column(Text)

    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    tags = relationship("ReactionImageTag",
                        secondary=reaction_images_tags_join_table,
                        backref="images")

    def __repr__(self):
        return "<ReactionImage(id='{}', url='{}', name='{}')>".format(self.id, self.url, self.name)
