#!/usr/bin/env sh

set -ex

cleanup() {
  docker-compose rm -fsv db-test rabbitmq-test
}

cleanup

docker-compose up -d db-test rabbitmq-test

trap cleanup EXIT

docker-compose run --rm test ./scripts/wait-for.py DATABASE_URL
docker-compose run --rm test ./scripts/wait-for.py RABBITMQ_URL
docker-compose run --rm test alembic upgrade head
docker-compose run --rm test
