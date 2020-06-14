# Cloud Services

I can optionally rely on managed cloud services to enable that sweet, sweet production scalability and reliability.
In tech meme language: you could say I am Cloud Native™.

⚠ When adding new features, please implement them in a way where they
can be tested and run without any cloud credentials. Thank you!

## Google Cloud Platform (GCP)

Right now I use GCP Storage to store uploaded images for production.
See [the file uploads skill](../kaori/skills/file_uploads).

Set the `GCLOUD_SERVICE_ACCOUNT_INFO` environment variable to a 
base64 encoded JSON service account key. See [the annotated default config file](../config/kaori.py) for instructions.
