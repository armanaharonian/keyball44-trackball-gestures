#!/usr/bin/env bash
# Opens the Trackball Tuner in your browser: change the trackball settings with
# buttons, then build and flash with one click. Runs at http://127.0.0.1:8045/
# Leave this window open while you use it; press Ctrl+C here to stop it.
set -euo pipefail
cd "$(dirname "$0")"

[ -x tools/.venv/bin/python ] || { echo "Run ./setup.sh first." >&2; exit 1; }
exec tools/.venv/bin/python tools/tuner/server.py "$@"
