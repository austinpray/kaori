from abc import ABC, abstractmethod
from tempfile import SpooledTemporaryFile


class FileUploader(ABC):

    # TODO: relax the file param down to just a regular stream or something.
    # No reason for it to be that strict
    @abstractmethod
    def upload(self, remote_name: str, file: SpooledTemporaryFile) -> str:
        """Upload a file to a file storage provider.

        If the user uploads a file with a name like 'Screen Shot 2020-06-05 at 4.21.07 PM.png', you will probably want
        to provide a `remote_name` like 'c7061b37b1d033dd-screen-shot-2020-06-05-at-4-21-07-pm.png' or something.

        Args:
            remote_name: the desired remote file name
            file: the file object to be uploaded

        Returns:
            str: The publicly accessible file URL

        """
        raise NotImplementedError
