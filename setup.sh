#!/usr/bin/env bash
# One-time setup. Downloads the holykeebs firmware source this keymap builds on
# (pinned to the versions it was tested with) and the Python library the flash
# and tuner tools use to talk to the keyboard.
#
# Usage: ./setup.sh     (safe to run again; it skips what's already there)
set -euo pipefail
cd "$(dirname "$0")"

VIAL_QMK_URL="https://github.com/holykeebs/vial-qmk.git"
VIAL_QMK_COMMIT="046431b684aedad1039c172f7077408c2afb1764"
USERSPACE_URL="https://github.com/holykeebs/qmk-userspace.git"
USERSPACE_COMMIT="d73078976d3bdd8d24e34c3efe720ea8fc4cf024"

step() { printf '\n\033[1m==> %s\033[0m\n' "$1"; }
need() {
  command -v "$1" >/dev/null 2>&1 || { printf '\nMissing: %s\n%s\n' "$1" "$2" >&2; exit 1; }
}

step "Checking the tools you need"
need git "Install Apple's command line tools: xcode-select --install"
need python3 "Install Apple's command line tools: xcode-select --install"
need docker "Install Docker Desktop from https://www.docker.com/products/docker-desktop/ and open it once."
echo "git, python3 and docker are installed."

fetch() {
  local dir=$1 url=$2 commit=$3
  if [ -d "$dir/.git" ]; then
    echo "$dir is already downloaded."
  else
    git clone "$url" "$dir"
  fi
  git -C "$dir" -c advice.detachedHead=false checkout -q "$commit"
}

step "Downloading the holykeebs Vial firmware (about 2 GB, takes a few minutes)"
fetch vial-qmk "$VIAL_QMK_URL" "$VIAL_QMK_COMMIT"
git -C vial-qmk submodule update --init --recursive

step "Downloading the holykeebs userspace (trackball and OLED code)"
fetch qmk-userspace "$USERSPACE_URL" "$USERSPACE_COMMIT"

step "Installing the Python library for talking to the keyboard"
if [ ! -x tools/.venv/bin/python ]; then
  python3 -m venv tools/.venv
fi
tools/.venv/bin/pip -q install hidapi
echo "Done."

step "Setup finished"
cat <<'EOF'
Next steps (the README explains each one):
  1. Save your current layout from Vial into the layouts folder.
  2. ./build.sh
  3. ./flash.sh
EOF
