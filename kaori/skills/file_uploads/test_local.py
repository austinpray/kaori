from .local import LocalFileUploader
from pathlib import Path
from urllib.parse import urljoin, urlparse
from tempfile import TemporaryDirectory, SpooledTemporaryFile
from uuid import uuid4


import sys

def test_local_file_uploader():
    upload_path = TemporaryDirectory(prefix='test_fu_local_').name
    #upload_path = 'static/tmp/img'
    local = LocalFileUploader(display_base='https://bogus.kaori.io',
                              upload_path=upload_path)

    fixture = Path(__file__)\
        .parent\
        .joinpath('../../../tests/fixtures/kaori.png')\
        .read_bytes()
    tmp = SpooledTemporaryFile(mode='wb+')
    tmp.write(fixture)
    tmp.seek(0)
    name = f'test-{uuid4()}-kaori.png'

    public = local.upload(name, tmp)

    uploaded_path = Path(upload_path).joinpath(Path(urlparse(public).path).name)
    assert public.startswith('https://bogus.kaori.io')
    assert public.endswith(name)
    assert uploaded_path.exists()
    print(uploaded_path.stat(), file=sys.stderr)
    assert uploaded_path.stat().st_size > 100




