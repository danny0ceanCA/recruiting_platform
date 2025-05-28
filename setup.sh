#!/usr/bin/env bash
# ------------------------------------------------------------
# setup.sh – offline bootstrap for Codex & local CI
# Installs Python deps from ./vendor without touching the Internet
# ------------------------------------------------------------
set -euo pipefail
echo "🔧  Bootstrapping offline …"

# 0) (Codex runs as root) – make sure basic build tools exist
if command -v apt-get >/dev/null 2>&1; then
  export DEBIAN_FRONTEND=noninteractive
  apt-get update -y
  apt-get install -y build-essential libpq-dev python3-dev cargo
fi

# 1) Python virtual environment
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip wheel

# 2) Install every package from the local wheel-house
pip install --no-index --find-links vendor -r requirements.txt

# 3) Optional: seed a local SQLite DB for tests (safe if file missing)
[ -f "./app/db/init_db.py" ] && python ./app/db/init_db.py || true

echo "✅  Setup complete."
