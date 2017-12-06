#!/usr/bin/env python

from cryptography.fernet import Fernet
key = Fernet.generate_key().decode('ascii')
print(key)
