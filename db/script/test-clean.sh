#!/usr/bin/env bash
#shellcheck disable=SC2039

set -euo pipefail

psql --user flow --no-align --list | \
    awk -F'|' '/^test/ {print $1}' | \
    while read -r dbname
    do
	psql --user flow -c "DROP DATABASE ${dbname}"
    done

echo "Done"
