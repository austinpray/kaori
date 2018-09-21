FROM python:3.6

ENV KIZ_DOCKER_VERSION 1.0.0
WORKDIR /kizuna

RUN apt-get update \
    && apt-get install -y --no-install-recommends vim graphviz \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# maint deps
RUN pip install pip-tools

# heavy deps
RUN pip install spacy
RUN python -m spacy download en

# regular deps
COPY requirements.in requirements.txt ./
RUN pip install -r requirements.txt

COPY vendor ./
RUN pip install -e vendor/python-slacktools
