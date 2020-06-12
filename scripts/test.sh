#!/usr/bin/env sh

set -ex


export DATABASE_URL="postgresql://kaori:kaori@db-test:5432/kaori"
export RABBITMQ_URL="amqp://guest:guest@rabbitmq-test:5672/%2F"


docker-compose up -d db-test rabbitmq-test

docker-compose run --rm test ./scripts/wait-for db-test:5432 -- echo "db up!"
docker-compose run --rm test ./scripts/wait-for rabbitmq-test:5672 -- echo "rabbitmq up!"
docker-compose run --rm -e DATABASE_URL test alembic upgrade head
docker-compose run --rm -e DATABASE_URL -e RABBITMQ_URL test
