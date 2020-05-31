from abc import ABC, abstractmethod
from os import path
from secrets import token_urlsafe
from shutil import copyfileobj
from tempfile import SpooledTemporaryFile
from urllib.parse import urljoin


class FileUploader(ABC):

    @abstractmethod
    def upload(self, remote_name: str, file: SpooledTemporaryFile) -> str:
        raise NotImplementedError


class LocalFileUploader(FileUploader):
    """ Used for testing and such """

    def __init__(self,
                 display_base='http://localhost:8081',
                 upload_path='static/tmp/img') -> None:
        self.display_base = display_base
        self.upload_path = upload_path

    def upload(self, remote_name: str, file: SpooledTemporaryFile) -> str:
        file_name = f'{token_urlsafe()}-{remote_name}'
        file_path = path.join(self.upload_path, file_name)
        with open(file_path, 'w+b') as dest:
            copyfileobj(file, dest)

        return urljoin(self.display_base, file_name)
