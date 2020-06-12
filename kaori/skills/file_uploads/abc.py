from abc import ABC, abstractmethod
from tempfile import SpooledTemporaryFile


class FileUploader(ABC):

    @abstractmethod
    def upload(self, remote_name: str, file: SpooledTemporaryFile) -> str:
        raise NotImplementedError
