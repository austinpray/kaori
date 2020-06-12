from tempfile import SpooledTemporaryFile

from .abc import FileUploader

class GCloudStorageUploader(FileUploader):
    def upload(self, remote_name: str, file: SpooledTemporaryFile) -> str:
        pass

