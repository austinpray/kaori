from abc import ABC, abstractmethod
from tempfile import SpooledTemporaryFile


class FileUploader(ABC):

    # TODO: relax the file param down to just a regular stream or something.
    # No reason for it to be that strict
    @abstractmethod
    def upload(self, remote_name: str, file: SpooledTemporaryFile) -> str:
        raise NotImplementedError
