from abc import ABC, abstractproperty, abstractmethod


class Adapter(ABC):

    @abstractproperty
    def provides(self):
        raise NotImplementedError

    @abstractproperty
    def handles(self):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def convert_payload(payload):
        raise NotImplementedError
