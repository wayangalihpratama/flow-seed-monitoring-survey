#!/usr/bin/env bash
#shellcheck disable=SC2016

set -eu
DATABASES='flow_monitoring'

for DB in ${DATABASES}
do
    docker-compose exec -T db bash -c "pg_dump --user flow --clean --create --format plain ${DB} > /docker-entrypoint-initdb.d/001-init-${DB}.sql;"
    echo "Export ${DB} done"
done
