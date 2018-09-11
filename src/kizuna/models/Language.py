from sqlalchemy import Column, Integer, String

from src.kizuna.models.Models import Base


class Language(Base):
    __tablename__ = 'languages'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    bcp47 = Column('bcp47', String)

    def __repr__(self):
        return f"<Language(id='{self.id}', name='{self.name}')>"
