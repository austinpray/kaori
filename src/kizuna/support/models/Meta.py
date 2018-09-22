from sqlalchemy import Column, Integer, String

from . import Base


class Meta(Base):
    __tablename__ = 'meta'

    id = Column(Integer, primary_key=True)
    key = Column(String, index=True, unique=True)
    value = Column(String)

    def __repr__(self):
        return "<Meta(id='{}', key='{}', value='{}')>".format(self.id, self.key, self.value)
