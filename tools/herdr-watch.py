"""Tells the keyboard whether the herdr terminal (Ghostty) is the front app.

Polls the front app on macOS and, when it changes, sends HERDR_MODE_MSG (0x7E)
over raw HID (usage page 0xFF60). In herdr mode the firmware turns ball motion
on layer 0 into pane focus moves. Reconnects when the keyboard is unplugged.

Usage: herdr-watch.py [AppName]   (default: Ghostty)
"""
import subprocess
import sys
import time

import hid

APP = sys.argv[1] if len(sys.argv) > 1 else "Ghostty"
MSG = 0x7E
VID, PID = 0xC3AC, 0x3143


def front_app():
    out = subprocess.run(
        ["osascript", "-e", 'tell application "System Events" to get name of first process whose frontmost is true'],
        capture_output=True, text=True,
    ).stdout.strip()
    return out


def open_dev():
    paths = [d["path"] for d in hid.enumerate(VID, PID) if d["usage_page"] == 0xFF60]
    if not paths:
        return None
    dev = hid.device()
    dev.open_path(paths[0])
    return dev


dev = None
sent = None
while True:
    want = front_app() == APP
    if dev is None or want != sent:
        try:
            dev = dev or open_dev()
            if dev is not None:
                dev.write(b"\x00" + bytes([MSG, 1 if want else 0]) + bytes(30))
                dev.read(32, 500)
                sent = want
        except OSError:
            dev = None
            sent = None
    time.sleep(0.4)
