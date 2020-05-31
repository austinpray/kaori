import os
import sys
from mimetypes import guess_type
from pprint import pprint
from urllib.parse import urlparse
from kaori.support.slack_files import download_slack_file


from kaori.skills.file_uploads import LocalFileUploader
from kaori.worker import sc

file_id = sys.argv[1]

if not file_id:
    print('no file_id')
    exit(1)

slack_file = sc.api_call('files.info', file=file_id)


name, file = download_slack_file(file_id, slack_client=sc)

local = LocalFileUploader()
print(local.upload(name, file))
