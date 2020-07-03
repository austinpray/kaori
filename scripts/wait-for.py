#!/usr/bin/env python3
import socket
import sys
import os
import time
from urllib.parse import urlparse

url = os.getenv(sys.argv[1])

if not url:
    raise RuntimeError('No URL specified')

url = urlparse(url)

target = f'{url.hostname}:{url.port}'

print(f'waiting for {target}')

last_error = None

s = None

for i in range(30):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((url.hostname, int(url.port)))
        s.shutdown(socket.SHUT_RDWR)
        print(f'{target} is UP!')
        exit(0)
    except OSError as e:
        print('.', end='')
        last_error = e
        time.sleep(1)
    finally:
        if s:
            s.close()

print(f'given up on {target}')
print(last_error)
exit(1)
