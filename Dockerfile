FROM python:3.11.2-bullseye as base

WORKDIR /app

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.2.2 \
    PATH=/root/.local/bin:$PATH

# install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -\
 && poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
RUN mkdir -p kaori/ \
 && touch kaori/__init__.py \
 && poetry install --only main

FROM base as production

COPY . .

FROM base as development

# Mount for docker-in-docker
ENV DOCKER_BUILDKIT=1
VOLUME [ "/var/lib/docker" ]

RUN poetry install
