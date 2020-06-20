from os import path
from shutil import copyfileobj
from pathlib import Path
from tempfile import SpooledTemporaryFile
from urllib.parse import urljoin

from .abc import FileUploader


class LocalFileUploader(FileUploader):
    """ Used for testing and such """

    def __init__(self,
                 display_base='https://kaori-img.ngrok.io',
                 upload_path='static/tmp/img') -> None:
        self.display_base = display_base
        self.upload_path = upload_path

    def upload(self, remote_name: str, file: SpooledTemporaryFile) -> str:
        Path(self.upload_path).mkdir(parents=True, exist_ok=True)
        file_path = path.join(self.upload_path, remote_name)
        with open(file_path, 'w+b') as dest:
            copyfileobj(file, dest)

        return urljoin(self.display_base, remote_name)
