# File Upload Skill

I am happy to receive files and store them wherever you want.
This is particularly useful when needing to liberate files
uploaded to slack. This way we can store a reference to them in
a database.

## Local Filesystem

The simplest example is my [`LocalFileUploader`](./local.py).
This just takes a file and saves it to the local filesystem.
This is useful for testing my file handling capabilities offline without real cloud storage credentials.

⚠ I will enable this as the default provider if:
1. Your `KIZUNA_ENV` is set to `development`
2. You do not have any other providers enabled.

