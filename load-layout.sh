#!/usr/bin/env bash
# Sends a saved layout (.vil) to the keyboard and checks it. No flash needed.
#
# Usage: ./load-layout.sh layouts/starter.vil
set -euo pipefail
cd "$(dirname "$0")"

PY="tools/.venv/bin/python"
[ -x "$PY" ] || { echo "Run ./setup.sh first." >&2; exit 1; }
VIL="${1:?usage: ./load-layout.sh layouts/<file>.vil}"
[ -f "$VIL" ] || { echo "No such file: $VIL" >&2; exit 1; }

"$PY" tools/restore_vil.py "$VIL" | tail -1
"$PY" tools/restore_vil.py "$VIL" --dry | tail -1
