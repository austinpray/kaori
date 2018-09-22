import arrow
from sqlalchemy import Column, Integer, String, DateTime, func, Text

from . import Base


class ReactionImageTag(Base):
    __tablename__ = 'reaction_image_tags'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, unique=True)
    description = Column(Text)

    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    @staticmethod
    def maybe_create_tag(session, name):
        tag = session.query(ReactionImageTag).filter(ReactionImageTag.name == name).first()
        if tag:
            return tag

        tag = ReactionImageTag(name=name)
        session.add(tag)
        return tag

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': arrow.get(self.created_at).timestamp,
            'updated_at': arrow.get(self.updated_at).timestamp
        }

    def __repr__(self):
        return "<ReactionImageTag(id='{}', name='{}'>".format(self.id, self.name)
