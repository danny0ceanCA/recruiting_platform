#!/usr/bin/env bash
# setup.sh — Codex & offline compatible
set -euo pipefail
echo "🔧 Bootstrapping …"

# 1) Pick the right python
if command -v python3 &>/dev/null; then
  PY=python3
elif command -v python &>/dev/null; then
  PY=python
else
  echo "No python in PATH" >&2
  exit 1
fi

# 2) Create venv
$PY -m venv .venv

# 3) Activate venv (handles Windows + Linux)
if [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
elif [ -f .venv/Scripts/activate ]; then
  source .venv/Scripts/activate
else
  echo "Can't find venv activate script" >&2
  exit 1
fi

# 4) Upgrade pip & install from vendor/
$PY -m pip install --no-index --find-links vendor pip wheel


if [ ! -d vendor ]; then
  echo "❌ vendor/ directory missing – cannot install offline packages"
  exit 1
fi

pip install --no-index --find-links vendor -r requirements.txt

echo "✅ Setup complete (offline)"
