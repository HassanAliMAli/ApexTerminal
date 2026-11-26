#!/usr/bin/env bash
set -euo pipefail
: "${RUNNER_TEMP:?GitHub Actions runner required}" "${GITHUB_ENV:?GitHub Actions runner required}"
tools=$(mktemp -d "$RUNNER_TEMP/apex-test-tools.XXXXXXXX")
cd "$tools"
download() {
  curl --proto '=https' --retry 3 --fail --silent --show-error --location "$1" --output "$2"
  printf '%s  %s\n' "$3" "$2" | sha256sum --check
}

download https://github.com/valkey-io/valkey/archive/refs/tags/9.1.2.tar.gz valkey.tar.gz \
  19c23908e7d57e8d91ef85b41f5646307582f10f4f0fb999bbf89ed24ec9c983
tar -xzf valkey.tar.gz
make -C valkey-9.1.2 -j2 MALLOC=libc BUILD_TLS=no valkey-server
{
  printf 'APEX_TEST_MYSQLD=%s\n' /usr/sbin/mysqld
  printf 'APEX_TEST_VALKEY=%s\n' "$tools/valkey-9.1.2/src/valkey-server"
} >> "$GITHUB_ENV"

case "${1:-backend}" in
  browser) ;;
  backend)
    mysql=mysql-8.4.9-linux-glibc2.28-x86_64-minimal
    download "https://cdn.mysql.com/archives/mysql-8.4/$mysql.tar.xz" mysql.tar.xz \
      d0142fc30e04bae7f15a46567238adf8956acccd35c5bca6e448322644536e3d
    tar -xJf mysql.tar.xz
    download https://github.com/fsouza/fake-gcs-server/releases/download/v1.56.1/fake-gcs-server_1.56.1_Linux_amd64.tar.gz gcs.tar.gz \
      0f2f9f6884417acd5cc27126a9aa237ccc627372a4aa5008b399641de6db9469
    tar -xzf gcs.tar.gz fake-gcs-server
    libaio=$(ldconfig -p | awk '/libaio.so.1/ && !path {path=$NF} END {print path}')
    test -n "$libaio"
    ln -s "$libaio" libaio.so.1
    {
      printf 'LD_LIBRARY_PATH=%s\n' "$tools${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
      printf 'APEX_TEST_MYSQL84D=%s\n' "$tools/$mysql/bin/mysqld"
      printf 'APEX_TEST_INITDB=%s\n' /usr/lib/postgresql/16/bin/initdb
      printf 'APEX_TEST_GCS=%s\n' "$tools/fake-gcs-server"
    } >> "$GITHUB_ENV"
    ;;
  *) exit 2 ;;
esac
