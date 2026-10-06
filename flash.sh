#!/usr/bin/env bash
# Installs ./firmware.uf2 on the half with the USB cable, then puts your layout
# back (every new build makes Vial reset the keys to defaults).
#
# Usage: ./flash.sh                     uses the newest .vil in layouts/
#        ./flash.sh layouts/my.vil      uses that layout
#
# 1. Refuses to continue unless the keyboard matches the layout exactly, so
#    nothing unsaved in Vial is lost.
# 2. Turns the key under P on the right half (matrix [7,1]) into the boot key
#    for a moment; you press it once.
# 3. Copies the firmware to the RPI-RP2 drive, waits for the keyboard to come
#    back, restores the layout (which also puts that key back) and checks it.
#
# macOS only (it waits for the RPI-RP2 drive and the USB device by name).
set -euo pipefail
cd "$(dirname "$0")"

PY="tools/.venv/bin/python"
UF2="$PWD/firmware.uf2"

[ -x "$PY" ] || { echo "Run ./setup.sh first." >&2; exit 1; }
[ -f "$UF2" ] || { echo "No firmware.uf2 yet. Run ./build.sh first." >&2; exit 1; }

VIL="${1:-$(ls -1t layouts/*.vil 2>/dev/null | head -1)}"
[ -n "$VIL" ] && [ -f "$VIL" ] || {
  echo "No layout found. Save your layout from Vial (File → Save current layout) into the layouts folder." >&2
  exit 1
}

echo "Checking the keyboard against $VIL..."
if ! "$PY" tools/restore_vil.py "$VIL" --dry | tail -1 | grep -q "would change 0 entries"; then
  echo "" >&2
  echo "The keyboard differs from $VIL, so flashing now would lose those keys." >&2
  echo "Open Vial, use File → Save current layout to save it into the layouts folder," >&2
  echo "close Vial, and run ./flash.sh again." >&2
  exit 1
fi

"$PY" - <<'EOF'
import hid
path = [d["path"] for d in hid.enumerate(0xC3AC, 0x3143) if d["usage_page"] == 0xFF60][0]
dev = hid.device()
dev.open_path(path)
dev.write(b"\x00" + bytes([0x05, 0, 7, 1, 0x7C, 0x00]) + bytes(26))  # layer 0 [7,1] = QK_BOOT
dev.read(32, 1000)
EOF

echo "Press the boot key now: right half, bottom row, the outermost key (under P)."
until [ -d /Volumes/RPI-RP2 ]; do sleep 1; done
sleep 1
cp -X "$UF2" /Volumes/RPI-RP2/ || true # errors once the drive ejects itself mid-copy
echo "Flashed. Waiting for the keyboard..."

until ioreg -p IOUSB -l -w0 | grep -q '"USB Product Name" = "Keyball44"'; do sleep 1; done
sleep 3

"$PY" tools/restore_vil.py "$VIL" | tail -1
"$PY" tools/restore_vil.py "$VIL" --dry | tail -1
