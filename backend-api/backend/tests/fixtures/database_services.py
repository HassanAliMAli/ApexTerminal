import pytest

from .base import _configure_test_settings, _reinitialize_rq_queue
from .native_services import LOOPBACK, mysql_instance


@pytest.fixture(scope="session")
def db_services(tmp_path_factory, native_valkey):
    with mysql_instance(tmp_path_factory.mktemp("mysql")) as mysql_port:
        _configure_test_settings(
            mysql_host=LOOPBACK,
            mysql_port=mysql_port,
            redis_host=LOOPBACK,
            redis_port=native_valkey,
        )
        _reinitialize_rq_queue()
        yield
