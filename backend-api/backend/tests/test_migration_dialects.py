from __future__ import annotations

import os
import subprocess
import sys
import tempfile

import sqlalchemy as sa

from tests.fixtures.native_services import LOOPBACK, mysql_instance

_BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_MIN_TABLES = 38


def _base_env() -> dict[str, str]:
    return {
        "MODE": "test",
        "JWT_SECRET": "testsecretfortesting12345678901234",
        "WORKSPACE_AES_KEY": "d29ya3NwYWNlLXRlc3Qtc3VpdGUtYXQtcmVzdC1rZXk",
        "APPURL": "http://localhost:3000",
        "SELFURL": "http://localhost:8000",
        "BACKEND_CORS_ORIGINS": "http://localhost:3000",
        "PROMETHEUS": "0",
        "WORKERS": "1",
        "STORAGE_PROVIDER": "aws",
        "S3_ACCESS_KEY": "test",
        "S3_SECRET_KEY": "test",
        "S3_BUCKET_NAME": "test",
        "S3_FILE_BUCKET": "test",
        "S3_ENDPOINT_URL": "http://localhost",
        "FRONTENDURL": "http://localhost",
        "SUPPRESSED_API_ROUTERS": "[]",
        "SUPPRESSED_API_ROUTES": "[]",
        "WORKSPACE_AUTH_TOKEN": "test-token",
    }


def _run_alembic_upgrade(env_vars: dict[str, str]):
    env = {**os.environ, **env_vars}
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        cwd=_BACKEND_DIR,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"alembic upgrade head failed (rc={result.returncode}):\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result


def _alembic_head() -> str:
    from alembic.config import Config
    from alembic.script import ScriptDirectory

    config = Config(os.path.join(_BACKEND_DIR, "alembic.ini"))
    return ScriptDirectory.from_config(config).get_current_head()


def _inspect_and_verify(engine: sa.engine.Engine, dialect_name: str):
    inspector = sa.inspect(engine)
    tables = inspector.get_table_names()

    assert len(tables) >= _MIN_TABLES, (
        f"{dialect_name}: Expected at least {_MIN_TABLES} tables, got {len(tables)}: {sorted(tables)}"
    )

    errors: list[str] = []

    with engine.connect() as conn:
        for table_name in tables:
            if table_name == "alembic_version":
                continue

            try:
                columns = inspector.get_columns(table_name)
                assert len(columns) > 0, f"{dialect_name}: Table {table_name} has no columns"
            except Exception as exc:
                errors.append(f"{dialect_name}: Failed to reflect columns for {table_name}: {exc}")
                continue

            try:
                result = conn.execute(sa.text(f"SELECT * FROM {_quote(table_name, dialect_name)} LIMIT 1"))
                result.fetchall()
            except Exception as exc:
                errors.append(f"{dialect_name}: SELECT failed on {table_name}: {exc}")

        expected_head = _alembic_head()
        version = conn.execute(sa.text("SELECT version_num FROM alembic_version")).scalar()
        assert version == expected_head, f"{dialect_name}: Expected alembic version {expected_head}, got {version}"

    assert not errors, f"{dialect_name} type-mapping errors:\n" + "\n".join(errors)


def _quote(table_name: str, dialect_name: str) -> str:
    if dialect_name == "mysql":
        return f"`{table_name}`"
    return f'"{table_name}"'


def _verify_database_upgrade(dialect: str, driver: str, port: int, valkey_port: int):
    env_vars = {
        **_base_env(),
        "DATABASE_TYPE": dialect,
        "DB_HOST": LOOPBACK,
        "DB_PORT": str(port),
        "DB_NAME": "test_db",
        "READ_DB_USER": "root",
        "READ_DB_PASSWORD": "test_password",
        "WRITE_DB_USER": "root",
        "WRITE_DB_PASSWORD": "test_password",
        "REDIS_HOST": LOOPBACK,
        "REDIS_PORT": str(valkey_port),
        "REDIS_PASS": "",
    }
    result = _run_alembic_upgrade(env_vars)
    assert "Running upgrade" in result.stderr, f"No migrations ran:\n{result.stderr}"
    url = sa.URL.create(
        driver,
        username="root",
        password="test_password",
        host=LOOPBACK,
        port=port,
        database="test_db",
        query={"charset": "utf8mb4"} if dialect == "mysql" else {},
    )
    engine = sa.create_engine(url)
    try:
        _inspect_and_verify(engine, dialect)
    finally:
        engine.dispose()


class TestMySQLMigrations:
    def test_mysql_upgrade_head(self, tmp_path, native_valkey):
        with mysql_instance(tmp_path, binary_variable="APEX_TEST_MYSQL84D") as port:
            _verify_database_upgrade("mysql", "mysql+pymysql", port, native_valkey)


class TestPostgreSQLMigrations:
    def test_postgres_upgrade_head(self, native_postgres, native_valkey):
        _verify_database_upgrade("postgresql", "postgresql+pg8000", native_postgres, native_valkey)


class TestSQLiteMigrations:
    def test_sqlite_upgrade_head(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.db")

            env_vars = {
                **_base_env(),
                "DATABASE_TYPE": "sqlite",
                "DB_PATH": db_path,
                "REDIS_HOST": "127.0.0.1",
                "REDIS_PORT": "6379",
                "REDIS_PASS": "",
            }

            result = _run_alembic_upgrade(env_vars)
            assert "Running upgrade" in result.stderr, f"No migrations ran:\n{result.stderr}"

            url = f"sqlite:///{db_path}"
            engine = sa.create_engine(url)
            try:
                _inspect_and_verify(engine, "sqlite")
            finally:
                engine.dispose()
