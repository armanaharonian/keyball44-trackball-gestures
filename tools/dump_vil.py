"""Saves the keyboard's current keys, tap dances and QMK settings as a .vil.

Usage: dump_vil.py <out.vil>

The reverse of restore_vil.py: keycodes are written as raw 16-bit numbers,
which restore_vil.py accepts. Combos, macros, key overrides and alt-repeat keys
are written empty (restore_vil.py refuses a keyboard that uses combos).
"""
import json
import sys

import hid

OUT = sys.argv[1]
base = json.load(open("layouts/starter.vil"))

path = [d["path"] for d in hid.enumerate(0xC3AC, 0x3143) if d["usage_page"] == 0xFF60][0]
dev = hid.device()
dev.open_path(path)


def cmd(*b):
    dev.write(b"\x00" + bytes(b) + bytes(32 - len(b)))
    return bytes(dev.read(32, 1000))


assert cmd(0xFE, 0x05)[0] == 1, "keyboard is locked"
layers = cmd(0x11)[1]
layout = [
    [[(lambda r: (r[4] << 8) | r[5])(cmd(0x04, layer, row, col)) for col in range(6)] for row in range(8)]
    for layer in range(layers)
]

n_td = cmd(0xFE, 0x0D, 0x00)[0]
tap_dance = []
for idx in range(n_td):
    r = cmd(0xFE, 0x0D, 0x01, idx)[1:11]
    v = [int.from_bytes(r[i : i + 2], "little") for i in range(0, 8, 2)]
    tap_dance.append(v + [int.from_bytes(r[8:10], "little")])

settings = {}
for qsid in map(int, base["settings"]):
    r = cmd(0xFE, 0x0A, qsid & 0xFF, qsid >> 8)
    if r[0] == 0:
        width = 1 if base["settings"][str(qsid)] < 0x100 else 2
        settings[str(qsid)] = int.from_bytes(r[1:5], "little") & ((1 << (8 * width)) - 1)

out = dict(base, layout=layout, tap_dance=tap_dance, settings=settings)
json.dump(out, open(OUT, "w"))
print(f"saved {layers} layers, {n_td} tap dances, {len(settings)} settings to {OUT}")
