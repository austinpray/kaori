from pathlib import Path
from shutil import copyfileobj
from tempfile import SpooledTemporaryFile
from uuid import uuid4

import pytest
from google.cloud import storage
from google.oauth2 import service_account

from kaori import test_config
from .gcloud import GCloudStorageUploader


@pytest.mark.skipif(not test_config.USE_GCLOUD_STORAGE,
                    reason="no google cloud config specified")
def test_gcloud_upload():
    creds = service_account.Credentials.from_service_account_info(test_config.GCLOUD_SERVICE_ACCOUNT_INFO)
    bucket = storage.Client(project=creds.project_id, credentials=creds).bucket(test_config.IMAGES_BUCKET_GCLOUD)

    uploader = GCloudStorageUploader(bucket=bucket, base_path=test_config.IMAGES_BUCKET_PATH)

    f = SpooledTemporaryFile()
    with Path(__file__).parent.joinpath('../../../tests/fixtures/kaori.png').open(mode='rb') as img:
        copyfileobj(img, f)

    f.seek(0)
    public = uploader.upload(f'TEST-{uuid4()}-kaori.png', f)
    assert test_config.IMAGES_BUCKET_GCLOUD in public
    assert public.startswith('http')
    assert public.endswith('kaori.png')

    with pytest.raises(RuntimeError):
        uploader.upload('very.based', f)

