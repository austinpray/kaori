#!/usr/bin/env sh

set -ex

docker-compose up -d db-test rabbitmq-test

docker-compose run --rm test ./scripts/wait-for db-test:5432 -- echo "db up!"
docker-compose run --rm test ./scripts/wait-for rabbitmq-test:5672 -- echo "rabbitmq up!"
docker-compose run --rm test alembic upgrade head
docker-compose run --rm test
