from sqlalchemy import Column, String, Text, Integer, DateTime, func
from kizuna.models.Models import Base
import arrow


class FaxMessage(Base):
    __tablename__ = 'fax_messages'

    id = Column('id', Integer, primary_key=True)
    trigger_id = Column('trigger_id', String, unique=True, index=True)

    user_name = Column('user_name', String)
    user_id = Column('user_id', String)
    team_id = Column('team_id', String)
    text = Column('text', Text)

    created_at = Column(DateTime, default=func.current_timestamp())
    printed_at = Column(DateTime)

    def __repr__(self):
        return "<FaxMessage(id='{}', user_name='{}', text='{}')>".format(self.id,
                                                                         self.user_name,
                                                                         self.text)

    def to_json_serializable(self):
        return {
            'id': self.id,
            'trigger_id': self.trigger_id,
            'user_name': self.user_name,
            'user_id': self.user_id,
            'team_id': self.team_id,
            'text': self.text,
            'created_at': arrow.get(self.created_at).timestamp,
            'printed_at': arrow.get(self.printed_at).timestamp
        }
