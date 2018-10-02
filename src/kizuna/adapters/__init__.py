from abc import ABC, abstractproperty


class Adapter(ABC):

    @abstractproperty
    def provides(self):
        raise NotImplementedError

    @abstractproperty
    def handles(self):
        raise NotImplementedError
