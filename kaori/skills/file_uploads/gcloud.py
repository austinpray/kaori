from tempfile import SpooledTemporaryFile
from pathlib import Path
from mimetypes import guess_type

from .abc import FileUploader


class GCloudStorageUploader(FileUploader):
    def __init__(self, bucket, base_path) -> None:
        self.bucket = bucket
        self.base_path = Path(base_path.lstrip('/'))

    def upload(self, remote_name: str, file: SpooledTemporaryFile) -> str:
        content_type = guess_type(remote_name)[0]
        if not content_type:
            raise RuntimeError(f'cannot guess type of {remote_name}')

        blob = self.bucket.blob(str(self.base_path.joinpath(remote_name)))

        blob.upload_from_file(file, content_type=content_type)

        return blob.public_url


