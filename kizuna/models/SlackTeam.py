from sqlalchemy import Column, Integer, String

from kizuna.models.Models import Base


class SlackTeam(Base):
    __tablename__ = 'slack_teams'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)

    def __repr__(self):
        return f"<SlackTeam(id='{self.id}', name='{self.name}')>"
