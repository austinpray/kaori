from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, DECIMAL, Boolean
from sqlalchemy.orm import relationship

from kizuna.models.Models import Base


class KKredsTransaction(Base):
    __tablename__ = 'kkreds_transactions'

    id = Column('id', Integer, primary_key=True)
    from_user_id = Column('from_user_id', Integer, ForeignKey('users.id'))
    from_user = relationship("User", foreign_keys=[from_user_id], backref="kkred_debits")
    to_user_id = Column('to_user_id', Integer, ForeignKey('users.id'))
    to_user = relationship("User", foreign_keys=[to_user_id], backref="kkred_credits")
    amount = Column('amount', DECIMAL, nullable=False)
    is_mined = Column('is_mined', Boolean, default=False)

    created_at = Column(DateTime, default=func.current_timestamp())

    def __repr__(self):
        return "<KKredsTransaction(id='{}', from_user='{}', to_user='{}')>".format(self.id,
                                                                                   self.from_user.name,
                                                                                   self.to_user.name)
