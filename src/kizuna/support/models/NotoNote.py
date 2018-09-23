from textwrap import shorten

from sqlalchemy import Column, Integer, BigInteger, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from . import Base


class NotoNote(Base):
    __tablename__ = 'noto_notes'

    id = Column('id', BigInteger, primary_key=True)
    parent_id = Column('parent_id', BigInteger)
    slack_team = relationship("NotoNote", foreign_keys=[parent_id])

    slack_message_id = Column('slack_message_id', BigInteger, ForeignKey('slack_messages.id')),
    slack_message = relationship("SlackMessage", foreign_keys=[slack_message_id])

    user_id = Column('user_id', Integer, ForeignKey('users.id')),
    user = relationship("User", foreign_keys=[user_id])

    text = Column('text', Text),
    description = Column('description', Text),
    deleted = Column('deleted', Boolean),
    created_at = Column('created_at', DateTime),

    def __repr__(self):
        return f"<NotoNote (id='{self.id}', parent_id='{self.parent_id}' text='{shorten(self.text, 10)}')>"
