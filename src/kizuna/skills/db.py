from sqlalchemy.orm import sessionmaker

from kizuna.support.utils import db_session_scope


class DB:
    def __init__(self, make_session: sessionmaker) -> None:
        self.make_session = make_session

    def session_scope(self):
        return db_session_scope(self.make_session)
