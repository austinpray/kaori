#!/usr/bin/env sh

set -ex


export DATABASE_URL="postgresql://kaori:kaori@db-test:5432/kaori"

docker-compose up -d db-test

docker-compose run --rm test ./scripts/wait-for db-test:5432 -- echo "db up!"
docker-compose run --rm -e DATABASE_URL test alembic upgrade head
docker-compose run --rm -e DATABASE_URL test
