from __future__ import annotations

import os
import shutil
import socket
import subprocess
import time
from contextlib import contextmanager
from pathlib import Path

import pytest

LOOPBACK = "127.0.0.1"


def executable(variable: str, default: str) -> str:
    name = os.environ.get(variable, default)
    path = shutil.which(name)
    if path is None:
        pytest.fail(f"Install {default} or set {variable} to its native executable")
    return str(Path(path).resolve())


def free_port() -> int:
    with socket.socket() as probe:
        probe.bind((LOOPBACK, 0))
        return probe.getsockname()[1]


def initialize(args: list[str], log: Path) -> None:
    with log.open("wb") as output:
        result = subprocess.run(args, stdout=output, stderr=subprocess.STDOUT, timeout=90, check=False)
    if result.returncode:
        pytest.fail(log.read_text(errors="replace")[-4000:])


@contextmanager
def running(args: list[str], log: Path, ready, *, timeout: int = 60, cwd: Path | None = None, env=None):
    with log.open("wb") as output:
        process = subprocess.Popen(args, stdout=output, stderr=subprocess.STDOUT, cwd=cwd, env=env)
        try:
            until = time.monotonic() + timeout
            while time.monotonic() < until and process.poll() is None:
                if ready():
                    yield
                    return
                time.sleep(0.1)
            pytest.fail(f"{log.stem} failed to start (exit {process.poll()}):\n{log.read_text(errors='replace')[-4000:]}")
        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()


def tcp_ready(port: int) -> bool:
    try:
        with socket.create_connection((LOOPBACK, port), timeout=0.2):
            return True
    except OSError:
        return False


@contextmanager
def mysql_instance(directory: Path, *, binary_variable: str = "APEX_TEST_MYSQLD"):
    import pymysql

    mysqld = executable(binary_variable, "mysqld")
    data = directory / "data"
    args = [mysqld, "--no-defaults", f"--basedir={Path(mysqld).parent.parent}", f"--datadir={data}"]
    initialize([*args, "--initialize-insecure"], directory / "initialize.log")
    port = free_port()
    init_file = directory / "initialize.sql"
    init_file.write_text(
        "ALTER USER 'root'@'localhost' IDENTIFIED BY 'test_password';\n"
        "CREATE DATABASE test_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\n",
        encoding="utf-8",
    )

    def ready() -> bool:
        try:
            with pymysql.connect(
                host=LOOPBACK, port=port, user="root", password="test_password", database="test_db", connect_timeout=1
            ):
                return True
        except pymysql.err.OperationalError:
            return False

    with running(
        [
            *args,
            f"--bind-address={LOOPBACK}",
            f"--port={port}",
            f"--socket={directory / 'mysql.sock'}",
            f"--pid-file={directory / 'mysql.pid'}",
            f"--init-file={init_file}",
            "--mysqlx=OFF",
            "--skip-log-bin",
        ],
        directory / "mysql.log",
        ready,
    ):
        yield port


@contextmanager
def valkey_instance(directory: Path):
    valkey = executable("APEX_TEST_VALKEY", "valkey-server")
    port = free_port()
    with running(
        [valkey, "--bind", LOOPBACK, "--port", str(port), "--dir", str(directory), "--save", "", "--appendonly", "no"],
        directory / "valkey.log",
        lambda: tcp_ready(port),
    ):
        yield port


@pytest.fixture(scope="session")
def native_valkey(tmp_path_factory):
    with valkey_instance(tmp_path_factory.mktemp("valkey")) as port:
        yield port


@pytest.fixture
def native_postgres(tmp_path):
    import pg8000.dbapi

    initdb = executable("APEX_TEST_INITDB", "initdb")
    postgres = str(Path(initdb).with_name("postgres"))
    data = tmp_path / "data"
    password_file = tmp_path / "password"
    password_file.write_text("test_password\n", encoding="utf-8")
    initialize(
        [initdb, "-D", str(data), "-U", "root", "--auth=scram-sha-256", f"--pwfile={password_file}"],
        tmp_path / "initialize.log",
    )
    port = free_port()

    def ready() -> bool:
        try:
            connection = pg8000.dbapi.connect(
                host=LOOPBACK, port=port, user="root", password="test_password", database="postgres", timeout=1
            )
            connection.close()
            return True
        except (pg8000.dbapi.Error, OSError):
            return False

    with running(
        [postgres, "-D", str(data), "-h", LOOPBACK, "-p", str(port), "-k", str(tmp_path)],
        tmp_path / "postgres.log",
        ready,
    ):
        connection = pg8000.dbapi.connect(
            host=LOOPBACK, port=port, user="root", password="test_password", database="postgres"
        )
        try:
            connection.autocommit = True
            connection.cursor().execute("CREATE DATABASE test_db")
        finally:
            connection.close()
        yield port
