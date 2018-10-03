import os
import ujson as json
from pprint import pprint


def read_dev_info(dev_info_path):
    if not os.path.isfile(dev_info_path):
        print('startup: no dev file at "{}"'.format(dev_info_path))
        return {}

    dev_info = json.load(open(dev_info_path))
    print('startup: dev info loaded from "{}"'.format(dev_info_path))
    pprint(dev_info)
    return dev_info
