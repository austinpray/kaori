from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from kizuna.models.Models import Base


class SlackMessage(Base):
    __tablename__ = 'slack_messages'

    id = Column('id', BigInteger, primary_key=True)

    slack_team_id = Column('slack_team_id', String, ForeignKey('slack_teams.id')),
    slack_team = relationship("SlackTeam", foreign_keys=[slack_team_id])

    user_id = Column('user_id', Integer, ForeignKey('users.id')),
    user = relationship("User", foreign_keys=[user_id])

    channel = Column('channel', String, nullable=False),
    ts = Column('ts', String, nullable=False),
    text = Column('text', Text)

    def __repr__(self):
        return f"<SlackMessage(id='{self.id}', ts='{self.ts}')>"
