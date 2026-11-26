import argparse
import json
import os
import secrets
import ssl
import subprocess
import sys
from contextlib import ExitStack
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlsplit
from http.client import HTTPSConnection

from tests.fixtures.native_services import LOOPBACK, free_port, mysql_instance, running, tcp_ready, valkey_instance

BACKEND = Path(__file__).resolve().parent.parent
ROOT = BACKEND.parents[1]
FRONTEND = ROOT / "frontend"
AGENT = ROOT / "agent"
WEB_URL = "https://localhost:3000"
API_URL = "https://localhost:8000"
AGENT_URL = "https://localhost:7777"
ADMIN = "e2e-admin@example.com"
PYTHON = sys.executable


def run(command, *, cwd=BACKEND, env=None, stdin=None):
    subprocess.run(command, cwd=cwd, env=env, input=stdin, text=True, check=True)


def read_env(path: Path) -> dict[str, str]:
    return {
        key: value
        for line in path.read_text().splitlines()
        if (key := line.partition("=")[0]).isidentifier()
        for value in [line.partition("=")[2]]
    }


def ready_https(ca: Path, url: str) -> bool:
    target = urlsplit(url)
    connection = HTTPSConnection("localhost", target.port, context=ssl.create_default_context(cafile=ca), timeout=1)
    try:
        connection.request("GET", target.path)
        return connection.getresponse().status == 200
    except OSError:
        return False
    finally:
        connection.close()


def nginx_config(directory: Path, tls: Path, *, api_port: int, agent_port: int) -> Path:
    nginx = (FRONTEND / "tests/e2e/tls/nginx.conf").read_text()
    nginx = nginx.replace("http://web:8080", "http://127.0.0.1:13000")
    nginx = nginx.replace("http://api:8000", f"http://127.0.0.1:{api_port}")
    nginx = nginx.replace("http://agent:7777", f"http://127.0.0.1:{agent_port}")
    for port in (3000, 8000, 7777):
        nginx = nginx.replace(f"listen {port} ssl;", f"listen 127.0.0.1:{port} ssl;")
    nginx = nginx.replace("/etc/nginx/certs/", f"{tls}/")
    nginx = nginx.replace(
        "http {",
        "http {\n  access_log off;\n"
        + "".join(
            f'  {kind}_temp_path "{directory}/{kind}";\n' for kind in ("client_body", "proxy", "fastcgi", "uwsgi", "scgi")
        ),
        1,
    )
    path = directory / "tls.conf"
    path.write_text(f'daemon off;\npid "{directory}/tls.pid";\nerror_log stderr;\n{nginx}')
    return path


def frontend_config(directory: Path) -> Path:
    config = (FRONTEND / "nginx.conf").read_text()
    module = Path(os.environ.get("APEX_NGINX_JS_MODULE", "/usr/lib/nginx/modules/ngx_http_js_module.so"))
    config = config.replace("worker_processes auto;", "worker_processes 1;")
    config = config.replace("pid /tmp/nginx.pid;", f'pid "{directory}/web.pid";')
    mime_types = os.environ.get("APEX_NGINX_MIME_TYPES", "/etc/nginx/mime.types")
    config = config.replace("include mime.types;", f'include "{mime_types}";')
    config = config.replace("js_path /etc/nginx/njs/;", f'js_path "{FRONTEND}";')
    config = config.replace("listen 8080;", "listen 127.0.0.1:13000;")
    config = config.replace("root /usr/share/nginx/html;", f'root "{FRONTEND / "dist"}";')
    config = config.replace(
        "http {",
        "http {\n"
        + "".join(
            f'  {kind}_temp_path "{directory}/web-{kind}";\n'
            for kind in ("client_body", "proxy", "fastcgi", "uwsgi", "scgi")
        ),
        1,
    )
    path = directory / "web.conf"
    path.write_text(f'load_module "{module}";\n{config}')
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--interop", action="store_true")
    parser.add_argument("playwright", nargs="*")
    args = parser.parse_args()
    generated = [
        BACKEND / "envs/.env",
        BACKEND / "scripts/cfgs/config.toml",
        BACKEND / "user_create.json",
        AGENT / ".env",
    ]
    if any(path.exists() for path in generated):
        raise SystemExit("Run browser verification in a clean checkout without application settings")
    if any(tcp_ready(port) for port in (3000, 8000, 7777, 13000)):
        raise SystemExit("Browser verification ports are already in use")

    with TemporaryDirectory(prefix="apex-browser-") as temp, ExitStack() as stack:
        directory = Path(temp)
        for path in generated:
            stack.callback(path.unlink, missing_ok=True)
        for subdir in ("mysql", "valkey", "plugins"):
            (directory / subdir).mkdir()
        mysql = stack.enter_context(mysql_instance(directory / "mysql"))
        valkey = stack.enter_context(valkey_instance(directory / "valkey"))
        api, agent, mcp, stub = (free_port() for _ in range(4))
        tls = directory / "tls"
        upstream_tls = directory / "upstream-tls"
        make_tls = FRONTEND / "tests/e2e/make-tls.sh"
        run(["sh", str(make_tls), str(tls), "localhost"])
        run(["sh", str(make_tls), str(upstream_tls), "proxy-upstream.e2e.test"])
        old_umask = os.umask(0o077)
        try:
            run(
                [
                    PYTHON,
                    "-m",
                    "scripts.create_local_env",
                    "--no-extra-admins",
                    "--admin-email",
                    ADMIN,
                    "--entity-name",
                    "End-to-end",
                ]
            )
        finally:
            os.umask(old_umask)
        backend = {
            **os.environ,
            "MODE": "local",
            "DB_HOST": LOOPBACK,
            "DB_PORT": str(mysql),
            "DB_NAME": "test_db",
            "READ_DB_USER": "root",
            "WRITE_DB_USER": "root",
            "READ_DB_PASSWORD": "test_password",
            "WRITE_DB_PASSWORD": "test_password",
            "REDIS_HOST": LOOPBACK,
            "REDIS_PORT": str(valkey),
            "FOLDER_STORAGE_PATH": str(directory / "storage"),
            "APPURL": WEB_URL,
            "FRONTENDURL": WEB_URL,
            "SELFURL": API_URL,
            "BACKEND_CORS_ORIGINS": json.dumps([WEB_URL]),
            "DEFAULT_MCP_SERVERS": json.dumps(
                [{"id": "agent-tools", "name": "Agent Tools", "url": f"http://{LOOPBACK}:{mcp}/mcp"}]
            ),
            "WIDGET_PLUGINS_DIR": str(directory / "plugins"),
            "WIDGET_PLUGIN_PROXY_CA_FILE": str(upstream_tls / "ca.pem"),
            "WIDGET_PLUGIN_BACKENDS": json.dumps({"e2e-forecast": "http://localhost:7794"}),
        }
        run([PYTHON, "-m", "alembic", "upgrade", "head"], env=backend)
        run([PYTHON, "-m", "scripts.init_users"], env=backend)
        password = f"E2e-{secrets.token_urlsafe(24)}!1a"
        run([PYTHON, "-m", "scripts.init_users", "--new-password", ADMIN], env=backend, stdin=f"{password}\n")
        agent_env = {
            **os.environ,
            **read_env(AGENT / ".env"),
            "WORKSPACE_API_URL": f"http://{LOOPBACK}:{api}",
            "WORKSPACE_ORIGIN": WEB_URL,
            "WORKSPACE_PUBLIC_URL": API_URL,
            "AGENT_CORS_ORIGINS": WEB_URL,
            "REDIS_URL": f"redis://{LOOPBACK}:{valkey}",
            "DEFAULT_MODEL": "ollama:stub",
            "OLLAMA_BASE_URL": f"http://{LOOPBACK}:{stub}/api",
            "AGENT_EMBED_MODEL": "",
        }
        commands = (
            ("api", [PYTHON, "-m", "uvicorn", "main:app", "--host", LOOPBACK, "--port", str(api)], BACKEND, backend, api),
            ("worker", [PYTHON, "base_workers.py"], BACKEND, backend, None),
            ("stub", ["node", "tests/stub-model/server.ts"], AGENT, {**os.environ, "PORT": str(stub)}, stub),
            ("agent", ["node", "src/server.ts"], AGENT, {**agent_env, "PORT": str(agent)}, agent),
            ("mcp", ["node", "mcp-server/src/server.ts"], AGENT, {**agent_env, "MCP_PORT": str(mcp)}, mcp),
        )
        for name, command, cwd, env, port in commands:
            stack.enter_context(
                running(command, directory / f"{name}.log", lambda: port is None or tcp_ready(port), cwd=cwd, env=env)
            )
        nginx = os.environ.get("APEX_TEST_NGINX", "nginx")
        web_env = {
            **os.environ,
            "BACKEND_URL": API_URL,
            "AI_API_URL": AGENT_URL,
            "AI_COPILOT_ENABLED": "true",
            "ALLOW_HTML_JS_EXECUTION": "true",
            "UI_SHOW_COMPANION_MCP_MODE": "true",
            "CSP_EXTRA_SOURCES": "connect-src http://localhost:7793",
        }
        stack.enter_context(
            running(
                [nginx, "-p", str(directory), "-c", str(frontend_config(directory))],
                directory / "web.log",
                lambda: tcp_ready(13000),
                env=web_env,
            )
        )
        config_path = nginx_config(directory, tls, api_port=api, agent_port=agent)
        stack.enter_context(
            running(
                [nginx, "-p", str(directory), "-c", str(config_path)],
                directory / "tls.log",
                lambda: all(
                    ready_https(tls / "ca.pem", url)
                    for url in (f"{API_URL}/health", f"{WEB_URL}/", f"{AGENT_URL}/status")
                ),
            )
        )
        browser = {
            **os.environ,
            "NODE_EXTRA_CA_CERTS": str(tls / "ca.pem"),
            "E2E_USER_EMAIL": ADMIN,
            "E2E_USER_PASSWORD": password,
            "E2E_PLUGINS_DIR": str(directory / "plugins"),
            "E2E_PROXY_TLS_DIR": str(upstream_tls),
        }
        if args.interop:
            browser["E2E_INTEROP"] = "1"
            suites = ["plugin-interop.spec.ts"]
        else:
            browser["E2E_BACKENDS"] = "1"
            suites = []
        run(["npm", "exec", "--", "playwright", "test", *suites, *args.playwright], cwd=FRONTEND, env=browser)


if __name__ == "__main__":
    main()
