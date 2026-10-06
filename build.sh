#!/usr/bin/env bash
# Builds the firmware with Docker (the same QMK image holykeebs uses), so nothing
# needs installing on your computer. Output: ./firmware.uf2
#
# Usage: ./build.sh             this repo's trackball keymap, with OLED
#        OLED=no ./build.sh     same, without the OLED screen
#        ./build.sh --stock     holykeebs' original Vial keymap (to go back)
set -euo pipefail
cd "$(dirname "$0")"

IMAGE="ghcr.io/qmk/qmk_cli@sha256:2dc05fc9f32efebd6b05c2b8676ee548358bc7e151e9dbf4dac6b6eed4513b07"
OLED="${OLED:-yes}"
KEYMAP="trackball"
[ "${1:-}" = "--stock" ] && KEYMAP="vial"

if [ ! -d vial-qmk ] || [ ! -d qmk-userspace ]; then
  echo "The firmware source isn't downloaded yet. Run ./setup.sh first." >&2
  exit 1
fi
if ! docker info >/dev/null 2>&1; then
  echo "Docker isn't running. Open Docker Desktop (open -a Docker), wait for the whale icon" >&2
  echo "in the menu bar, then run ./build.sh again." >&2
  exit 1
fi

if [ "$KEYMAP" = "trackball" ]; then
  # The keymap lives in ./keymap; copy it to where QMK looks for keymaps.
  DEST="vial-qmk/keyboards/holykeebs/keyball44/keymaps/trackball"
  rm -rf "$DEST"
  mkdir -p "$DEST"
  cp keymap/* "$DEST/"
fi

echo "Building the $KEYMAP keymap (OLED=$OLED). This takes about a minute..."
docker run --rm \
  -v "$PWD":/work \
  -w /work/vial-qmk \
  -e QMK_USERSPACE=/work/qmk-userspace \
  "$IMAGE" \
  bash -c "git config --global --add safe.directory '*' && \
    make holykeebs/keyball44:$KEYMAP -e USER_NAME=holykeebs -e OLED=$OLED -j8"

cp "vial-qmk/holykeebs_keyball44_$KEYMAP.uf2" firmware.uf2
echo "Firmware ready: $PWD/firmware.uf2"
