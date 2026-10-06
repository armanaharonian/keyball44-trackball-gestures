"""Restores a Vial .vil backup (keymap, tap dances, QMK settings) over raw HID.

Usage: restore_vil.py <layout.vil> [--dry]   (--dry only reports differences)

Speaks the VIA/Vial raw HID protocol (usage page 0xFF60): VIA 0x04/0x05 get/set
keycode, Vial 0xFE 0x0D 0x01/0x02 get/set tap dance, 0xFE 0x0A/0x0B get/set QMK
setting (see vial-qmk/quantum/via.h and vial.h). Combos, macros, key overrides
and alt-repeat keys are not restored, so the script refuses a .vil that uses
them rather than letting a flash wipe them silently.
"""
import json
import sys

import hid

from keycodes import kc

VIL = sys.argv[1]
DRY = "--dry" in sys.argv

vil = json.load(open(VIL))

unsupported = [
    name
    for name, used in (
        ("combos", any(any(k != "KC_NO" for k in c) for c in vil.get("combo", []))),
        ("macros", any(vil.get("macro", []))),
        ("key overrides", any(o.get("trigger", "KC_NO") != "KC_NO" for o in vil.get("key_override", []))),
        ("alt-repeat keys", any(a.get("keycode", "KC_NO") != "KC_NO" for a in vil.get("alt_repeat_key", []))),
    )
    if used
]
if unsupported:
    sys.exit(f"{VIL} uses {', '.join(unsupported)}, which this script can't restore yet; extend it first.")

path = [d["path"] for d in hid.enumerate(0xC3AC, 0x3143) if d["usage_page"] == 0xFF60][0]
dev = hid.device()
dev.open_path(path)


def cmd(*b):
    dev.write(b"\x00" + bytes(b) + bytes(32 - len(b)))
    return bytes(dev.read(32, 1000))


assert cmd(0xFE, 0x05)[0] == 1, "keyboard is locked"

# Combos made in Vial but missing from the .vil would be lost on the next flash.
n_combo = cmd(0xFE, 0x0D, 0x00)[1]
if any(any(cmd(0xFE, 0x0D, 0x03, idx)[1:11]) for idx in range(n_combo)):
    sys.exit("The keyboard has combos; save them in a new .vil and extend this script first.")

layers = cmd(0x11)[1]  # id_dynamic_keymap_get_layer_count
changed = 0
for layer, rows in enumerate(vil["layout"][:layers]):
    for row, cols in enumerate(rows):
        for col, name in enumerate(cols):
            want = kc(name)
            if want is None:
                continue
            r = cmd(0x04, layer, row, col)
            have = (r[4] << 8) | r[5]
            if have != want:
                changed += 1
                print(f"L{layer} [{row},{col}] {have:#06x} -> {want:#06x} {name}")
                if not DRY:
                    cmd(0x05, layer, row, col, want >> 8, want & 0xFF)

n_td = cmd(0xFE, 0x0D, 0x00)[0]
for idx, td in enumerate(vil["tap_dance"][:n_td]):
    vals = [kc(x) for x in td[:4]] + [td[4]]
    payload = b"".join(v.to_bytes(2, "little") for v in vals)
    have = cmd(0xFE, 0x0D, 0x01, idx)[1:11]
    if have != payload:
        changed += 1
        print(f"TD{idx} {have.hex()} -> {payload.hex()} {td}")
        if not DRY:
            cmd(0xFE, 0x0D, 0x02, idx, *payload)

for qsid, value in vil.get("settings", {}).items():
    qsid = int(qsid)
    r = cmd(0xFE, 0x0A, qsid & 0xFF, qsid >> 8)
    if r[0] != 0:
        continue
    have = int.from_bytes(r[1:5], "little")
    # Settings are 1, 2 or 4 bytes wide; compare on the width the value needs.
    width = 1 if value < 0x100 else 2 if value < 0x10000 else 4
    have &= (1 << (8 * width)) - 1
    if have != value:
        changed += 1
        print(f"setting {qsid}: {have} -> {value}")
        if not DRY:
            cmd(0xFE, 0x0B, qsid & 0xFF, qsid >> 8, *value.to_bytes(4, "little"))

print(("would change" if DRY else "changed"), changed, "entries")
