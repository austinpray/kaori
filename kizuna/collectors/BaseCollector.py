from abc import ABC, abstractmethod


class BaseCollector(ABC):

    @abstractmethod
    def __init__(self, db_session_maker, slack_client=None) -> None:
        self.slack_client = slack_client
        self.db_session_maker = db_session_maker

    @abstractmethod
    def collect(self, message):
        pass
