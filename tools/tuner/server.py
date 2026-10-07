"""Trackball tuner: a local web page that edits the settings in keymap/keymap.c,
then builds and flashes with ./build.sh and ./flash.sh.

Usage: tools/.venv/bin/python tools/tuner/server.py [--port N] [--no-open]
Started by ./tuner.sh. Listens on 127.0.0.1 only. If the build or the check
before flashing fails, keymap.c is put back as it was.
"""
import json
import re
import socket
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
KEYMAP = ROOT / "keymap/keymap.c"
LAYOUTS = ROOT / "layouts"

DEFINE_RE = r"^(#\s*define\s+{name}\s+)(-?\d+)(\s*)$"
SETTINGS = ["BALL_POINTER_NUM", "BALL_POINTER_DEN", "BALL_SNIPE_NUM", "BALL_SNIPE_DEN", "BALL_SCROLL_DIVISOR",
            "APP_SWITCH_STEP", "APP_SWITCH_TIMEOUT_MS", "APP_SWITCH_GESTURE_GAP_MS", "APP_SWITCH_LOCK_TRAVEL",
            "BALL_KEY_STEP", "BALL_TRACK_STEP"]


def newest_layout():
    files = sorted(LAYOUTS.glob("*.vil"), key=lambda p: p.stat().st_mtime)
    return files[-1] if files else None


def read_settings():
    text = KEYMAP.read_text()
    values = {}
    for name in SETTINGS:
        m = re.search(DEFINE_RE.format(name=name), text, re.M)
        if m:
            values[name] = int(m[2])
    return values


def write_settings(text, changes):
    for name, value in changes.items():
        text, n = re.subn(DEFINE_RE.format(name=name), lambda m: f"{m[1]}{value}{m[3]}", text, count=1, flags=re.M)
        if n != 1:
            raise RuntimeError(f"Couldn't find {name} in keymap.c")
    return text


def run(args, timeout=30):
    r = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stdout + r.stderr).strip()


def docker_ready():
    try:
        return run(["docker", "info", "--format", "{{.ServerVersion}}"])[0] == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


class Job:
    def __init__(self):
        self.lock = threading.Lock()
        self.reset()

    def reset(self):
        self.state, self.stage, self.lines, self.error, self.press = "idle", None, [], None, False

    def log(self, line):
        with self.lock:
            self.lines.append(line.rstrip("\n"))
            if "Press the boot key" in line:
                self.press = True
            if line.startswith("Flashed."):
                self.press = False

    def snapshot(self):
        with self.lock:
            return {"state": self.state, "stage": self.stage, "lines": self.lines[-400:],
                    "error": self.error, "press": self.press}


JOB = Job()


def stream(args, stage):
    JOB.stage = stage
    JOB.log(f"$ {' '.join(args)}")
    p = subprocess.Popen(args, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in p.stdout:
        JOB.log(line)
    return p.wait()


def hint(output):
    if "keyboard is locked" in output:
        return "Vial (the app or vial.rocks) is connected to the keyboard. Close it and try again."
    if "differs from" in output:
        return ("The keyboard has key changes that aren't saved in a layout file. In Vial, use "
                "File → Save current layout to save it into the layouts folder, close Vial, and try again.")
    if "list index out of range" in output:
        return "The keyboard wasn't found over USB. Check the cable on the USB half."
    return None


def job(changes):
    original = KEYMAP.read_text()
    try:
        JOB.stage = "save"
        KEYMAP.write_text(write_settings(original, changes))
        JOB.log("Saved keymap.c: " + ", ".join(f"{k} = {v}" for k, v in changes.items()))

        JOB.stage = "docker"
        if not docker_ready():
            JOB.log("Docker isn't running; opening it...")
            run(["open", "-a", "Docker"])
            for _ in range(60):
                time.sleep(2)
                if docker_ready():
                    break
            else:
                raise RuntimeError("Docker didn't start within two minutes. Open Docker and try again.")
        JOB.log("Docker is running.")

        if stream(["./build.sh"], "build") != 0:
            KEYMAP.write_text(original)
            raise RuntimeError("The build failed, so nothing was flashed and keymap.c was put back as it was.")

        if stream(["./flash.sh"], "flash") != 0:
            out = "\n".join(JOB.lines[-25:])
            if any(line.startswith("Flashed.") for line in JOB.lines):
                raise RuntimeError((hint(out) or "The firmware was flashed, but restoring the layout failed.")
                                   + " Run ./load-layout.sh with your layout file.")
            KEYMAP.write_text(original)
            raise RuntimeError((hint(out) or "The flash failed.") + " Nothing was flashed; keymap.c was put back.")
        if not JOB.lines or JOB.lines[-1] != "would change 0 entries":
            raise RuntimeError("Flashed, but the layout check at the end didn't pass. "
                               "Run ./load-layout.sh with your layout file.")
        JOB.stage, JOB.state = "done", "done"
    except Exception as e:  # shown on the page
        JOB.error, JOB.state = str(e), "error"
        JOB.log("ERROR: " + str(e))


def apply(body):
    if JOB.state == "running":
        return {"ok": False, "error": "A build is already running."}
    current = read_settings()
    changes = {}
    for name, value in body.get("values", {}).items():
        if name not in SETTINGS or not isinstance(value, int) or not 0 < value <= 1_000_000:
            return {"ok": False, "error": f"{name}: must be a whole number above 0."}
        if current.get(name) != value:
            changes[name] = value
    if not changes:
        return {"ok": False, "error": "Nothing changed."}
    JOB.reset()
    JOB.state = "running"
    threading.Thread(target=job, args=(changes,), daemon=True).start()
    return {"ok": True}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send(self, status, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        try:
            if self.path in ("/", "/index.html"):
                return self.send(200, (HERE / "tuner.html").read_bytes(), "text/html; charset=utf-8")
            if self.path == "/style.css":
                return self.send(200, (HERE / "style.css").read_bytes(), "text/css; charset=utf-8")
            if self.path == "/api/settings":
                layout = newest_layout()
                return self.send(200, {"values": read_settings(), "layout": layout.name if layout else None,
                                       "busy": JOB.state == "running"})
            if self.path == "/api/job":
                return self.send(200, JOB.snapshot())
            self.send(404, {"error": "not found"})
        except Exception as e:
            self.send(500, {"ok": False, "error": str(e)})

    def do_POST(self):
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            if self.path == "/api/apply":
                return self.send(200, apply(body))
            self.send(404, {"error": "not found"})
        except Exception as e:
            self.send(500, {"ok": False, "error": str(e)})


def main():
    port = int(sys.argv[sys.argv.index("--port") + 1]) if "--port" in sys.argv else 8045
    url = f"http://127.0.0.1:{port}/"
    should_open = "--no-open" not in sys.argv

    with socket.socket() as s:
        if s.connect_ex(("127.0.0.1", port)) == 0:
            print(f"Already running at {url}", flush=True)
            if should_open:
                subprocess.run(["open", url])
            return

    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Trackball tuner running at {url}\nLeave this window open while you use it. Press Ctrl+C to stop.",
          flush=True)
    if should_open:
        threading.Timer(0.4, lambda: subprocess.run(["open", url])).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
