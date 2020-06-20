from hashlib import sha512
from typing import IO
from pathlib import Path


def hashed_file_name(path: str, file_hash: str) -> str:
    path = Path(path)
    return str(path.with_name(f'{path.stem}-{file_hash}{path.suffix}'))


_memory_page_size = 65536


def file_digest(file: IO[bytes],
                digest_algo=sha512,
                block_size=_memory_page_size) -> str:
    """
    # openssl dgst -sha512 -hex FILENAME

    We use sha512 cause it is faster on 64 bit processors for the chunk size we are targeting:
    # openssl speed sha256 sha512
    """

    file.seek(0)
    file_hash = digest_algo()
    while True:
        buffer = file.read(block_size)
        if len(buffer) == 0:
            break
        file_hash.update(buffer)
    file.seek(0)

    hexdigest = file_hash.hexdigest()
    return f'{file_hash.name}-{hexdigest}'
