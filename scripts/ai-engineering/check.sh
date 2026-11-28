set -eu
root="${AI_TOOLS_HOME:-$HOME/.local/share/apex-ai}"
export PATH="$root/bin:$root/npm/node_modules/.bin:$PATH"
export SEMGREP_SEND_METRICS=off
export OPENSPEC_TELEMETRY=0
case "${1:-health}" in
  health)
    missing=0
    for tool in opencode codex node npm uv gh openspec serena context7-mcp ast-grep semgrep gitleaks osv-scanner playwright playwright-mcp chrome-devtools-mcp k6; do
      if location=$(command -v "$tool"); then
        printf '%-24s %s\n' "$tool" "$location"
      else
        printf '%-24s %s\n' "$tool" missing >&2
        missing=1
      fi
    done
    exit "$missing"
    ;;
  config)
    python3 -c 'import json, os, pathlib, tomllib
home = pathlib.Path.home()
paths = [pathlib.Path(os.environ.get("CODEX_HOME", home / ".codex")) / "config.toml", pathlib.Path(os.environ.get("XDG_CONFIG_HOME", home / ".config")) / "opencode/opencode.json"]
for path, parse in zip(paths, (tomllib.loads, json.loads)):
    parse(path.read_text())
    print(path, "parsed")'
    ;;
  mcp)
    result=0
    codex mcp list || result=1
    for attempt in 1 2 3; do
      if ! output=$(opencode mcp list); then
        result=1
        break
      fi
      case "$output" in
        *"No MCP servers configured"*|"")
          if [ "$attempt" -lt 3 ]; then
            sleep 1
          else
            printf '%s\n' 'OpenCode did not report an MCP catalog. Check tool execution inside a session before changing configuration.' >&2
            result=1
          fi
          ;;
        *)
          printf '%s\n' "$output"
          break
          ;;
      esac
    done
    exit "$result"
    ;;
  browser)
    node scripts/ai-engineering/browser-smoke.cjs
    ;;
  backup)
    umask 077
    mkdir -p "$root/backups"
    destination=$(mktemp -d "$root/backups/config.XXXXXXXX")
    for file in config.toml AGENTS.md; do
      source="${CODEX_HOME:-$HOME/.codex}/$file"
      if [ -f "$source" ]; then install -D -m 600 "$source" "$destination/codex/$file"; fi
    done
    for file in opencode.json opencode.jsonc AGENTS.md; do
      source="${XDG_CONFIG_HOME:-$HOME/.config}/opencode/$file"
      if [ -f "$source" ]; then install -D -m 600 "$source" "$destination/opencode/$file"; fi
    done
    printf '%s\n' "$destination"
    ;;
  reproduce-npm)
    npm ci --prefix "$root/npm" --ignore-scripts --no-audit --no-fund
    ;;
  init)
    openspec init "${2:-.}" --scope project --tools agents --no-animation
    ;;
  setup-hook)
    UV_TOOL_DIR="$root/uv-tools" UV_TOOL_BIN_DIR="$root/bin" uv tool install pre-commit==4.5.1
    pre-commit validate-config
    pre-commit install
    ;;
  staged-secrets)
    gitleaks git --staged --redact=100 --no-banner .
    ;;
  secrets)
    result=0
    gitleaks git --redact=100 --no-banner . || result=1
    gitleaks git --staged --redact=100 --no-banner . || result=1
    exit "$result"
    ;;
  sast)
    semgrep scan --metrics=off --disable-version-check --jobs 2 --error --config scripts/ai-engineering/semgrep.yml frontend/src backend-api/backend agent/src
    ;;
  dependencies)
    osv-scanner scan source --offline -L frontend/package-lock.json -L agent/package-lock.json -L website/package-lock.json -L backend-api/backend/poetry.lock
    ;;
  *)
    printf 'Usage: bash %s {health|config|mcp|browser|backup|reproduce-npm|init [path]|setup-hook|staged-secrets|secrets|sast|dependencies}\n' "$0" >&2
    exit 2
    ;;
esac
