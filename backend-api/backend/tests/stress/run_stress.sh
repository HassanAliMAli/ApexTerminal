#!/usr/bin/env bash
set -euo pipefail

: "${BASE_URL:?Set BASE_URL to a running dedicated test API}"
: "${ADMIN_EMAIL:?Set ADMIN_EMAIL for the test account}"
: "${ADMIN_PASSWORD:?Set ADMIN_PASSWORD for the test account}"

if [[ ! "$BASE_URL" =~ ^https?://(localhost|127\.0\.0\.1)(:[0-9]+)?/?$ ]]; then
  printf 'The load simulator requires a localhost test API.\n' >&2
  exit 2
fi

directory=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
curl -fsS --max-time 5 -o /dev/null "${BASE_URL%/}/health"
exec "${PYTHON:-python3.13}" "$directory/load_simulator.py"
