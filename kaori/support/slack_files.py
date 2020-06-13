import os
import sys
from mimetypes import guess_type
from pprint import pprint
from tempfile import SpooledTemporaryFile
from typing import Tuple
from urllib.parse import urlparse

import requests


def download_slack_file(file_id: str, slack_client) -> Tuple[str, SpooledTemporaryFile]:
    slack_file = slack_client.api_call('files.info', file=file_id)

    url = slack_file.get('file').get('url_private')
    file_name = os.path.basename(urlparse(url).path)
    file_type = guess_type(url)[0]

    max_chunk = int(1e6)  # 1MiB

    tmp = SpooledTemporaryFile(suffix=file_name, mode='w+b', max_size=max_chunk)

    headers = {
        'user-agent': 'github.com/austinpray/kaori',
        'Authorization': f'Bearer {slack_client.token}',
    }

    with requests.get(url, headers=headers, stream=True) as resp:
        if resp.status_code != 200:
            raise RuntimeError('non-200 on image')
        content_type = resp.headers['content-type']
        if file_type not in content_type:
            raise RuntimeError(f'wrong filetype {content_type}, expected {file_type}')

        for chunk in resp.iter_content(chunk_size=max_chunk):
            tmp.write(chunk)

    tmp.seek(0)
    return file_name, tmp
