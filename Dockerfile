FROM python:3.11.0-bullseye as base

WORKDIR /app

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.2.2

# install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -\
 && echo 'export PATH=$PATH:$HOME/.poetry/bin' > /etc/profile.d/poetry.sh\
 && $HOME/.poetry/bin/poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
RUN mkdir -p kaori/ \
 && touch kaori/__init__.py \
 && $HOME/.poetry/bin/poetry install --no-dev

FROM base as production

COPY . .

FROM base as development

# Mount for docker-in-docker
ENV DOCKER_BUILDKIT=1
VOLUME [ "/var/lib/docker" ]

RUN $HOME/.poetry/bin/poetry install
