from kaori.skills.file_uploads import LocalFileUploader
from kaori.support.slack_files import download_slack_file
from kaori.worker import sc

import pytest

@pytest.mark.skip(reason="Can break if testbed slack goes unused for too long")
def test_download_slack_file():
    file_id = sc.api_call('files.list')['files'][0]['id']

    name, file = download_slack_file(file_id, slack_client=sc)

    local = LocalFileUploader()
    url = local.upload(name, file)

    assert url.endswith(name)
