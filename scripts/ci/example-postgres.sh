#!/usr/bin/env bash
set -euo pipefail
: "${RUNNER_TEMP:?GitHub Actions runner required}" "${GITHUB_ENV:?GitHub Actions runner required}"
port="${1:?port required}"
[[ "$port" == 55432 || "$port" == 55433 ]]
root=$(mktemp -d "$RUNNER_TEMP/example-postgres.XXXXXXXX")
cd "$root"
curl --proto '=https' --retry 3 --fail --silent --show-error --location \
  https://ftp.postgresql.org/pub/source/v18.6/postgresql-18.6.tar.bz2 --output postgresql.tar.bz2
printf '%s  %s\n' 555610c24d53e4316da5b7d3fc25c279d96856d5e0e23ee308c328c5fa881d9f postgresql.tar.bz2 \
  | sha256sum --check
tar -xjf postgresql.tar.bz2
(
  cd postgresql-18.6
  ./configure --prefix="$root/runtime" --without-icu --without-readline
  make -j2
  make install
)
password=$(openssl rand -hex 24)
printf '::add-mask::%s\n' "$password"
umask 077
printf '%s\n' "$password" > password
"$root/runtime/bin/initdb" -D "$root/data" -U postgres --auth=scram-sha-256 --pwfile="$root/password"
"$root/runtime/bin/pg_ctl" -D "$root/data" -l "$root/postgres.log" -w -t 30 \
  -o "-h 127.0.0.1 -p $port -k '$root'" start
printf 'postgresql://postgres:%s@127.0.0.1:%s/postgres\n' "$password" "$port" > postgres_url
printf 'SQL_EXPLORER_TEST_POSTGRES_FILE=%s\n' "$root/postgres_url" >> "$GITHUB_ENV"
