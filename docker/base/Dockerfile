FROM python:3.6

ENV KIZ_DOCKER_VERSION 1
WORKDIR /kizuna

RUN apt-get update \
    && apt-get install -y --no-install-recommends vim \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY vendor ./vendor
RUN pip install -e ./vendor/python-slacktools
