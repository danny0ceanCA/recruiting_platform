#!/usr/bin/env bash
# ------------------------------------------------------------
# setup.sh – works even when the Codex sandbox has NO internet
# ------------------------------------------------------------
set -euo pipefail
echo "🔧  Bootstrapping …"

# 0) Skip apt-get entirely; the Codex image already has gcc & libpq
#    If you ever need them, wrap in a timeout so failure is harmless:
# timeout 15s apt-get update || true

# 1) Virtual-env
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip wheel

# 2) Install backend deps from the local wheel-house
pip install --no-index --find-links vendor -r requirements.txt

# 3) Optional DB seed (safe if file absent)
[ -f "./app/db/init_db.py" ] && python ./app/db/init_db.py || true

echo "✅  Backend ready (offline)"
