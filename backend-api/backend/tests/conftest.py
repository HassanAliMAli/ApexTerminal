from os import environ

pytest_plugins = [
    "tests.fixtures.hooks",
    "tests.fixtures.native_services",
    "tests.fixtures.database_services",
    "tests.fixtures.migrations",
    "tests.fixtures.db",
    "tests.fixtures.clients",
    "tests.fixtures.mocks",
    "tests.fixtures.organization",
    "tests.fixtures.widget_plugins",
    "tests.fixtures.plugin_proxies",
    "tests.fixtures.plugin_backends",
]


environ["PYTEST_IS_RUNNING"] = "true"
