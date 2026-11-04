#!/usr/bin/env python3
"""
Full-page PNG renderer for HTML design artifacts.

Uses system Google Chrome's DevTools Protocol over a raw WebSocket implemented
with only the Python standard library. No npm install, no Playwright, no
Selenium, no browser download.

Usage:
    python3 render_cdp.py page.html --out ./shots
    python3 render_cdp.py ./pages --out ./shots --viewport desktop:1440x1000 --viewport mobile:390x844

Produces full-page PNGs at 2x device scale factor.
"""
import argparse
import base64
import json
import os
import pathlib
import socket
import struct
import subprocess
import sys
import time
import urllib.request

DEFAULT_VIEWPORTS = [
    ("desktop", 1440, 1000),
    ("mobile", 390, 844),
]


# --------------------------------------------------------------------------
# Minimal RFC6455 WebSocket client (stdlib only)
# --------------------------------------------------------------------------
class WS:
    def __init__(self, url):
        assert url.startswith("ws://"), url
        rest = url[5:]
        hostport, path = rest.split("/", 1)
        path = "/" + path
        host, port = hostport.split(":")
        self.sock = socket.create_connection((host, int(port)), timeout=60)
        key = base64.b64encode(os.urandom(16)).decode()
        req = (
            f"GET {path} HTTP/1.1\r\nHost: {hostport}\r\nUpgrade: websocket\r\n"
            f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\n"
            f"Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(req.encode())
        buf = b""
        while b"\r\n\r\n" not in buf:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise EOFError("handshake failed")
            buf += chunk
        self.buf = buf.split(b"\r\n\r\n", 1)[1]

    def _recv(self, n):
        while len(self.buf) < n:
            chunk = self.sock.recv(65536)
            if not chunk:
                raise EOFError
            self.buf += chunk
        out, self.buf = self.buf[:n], self.buf[n:]
        return out

    def send(self, data: str):
        payload = data.encode()
        mask = os.urandom(4)
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        n = len(payload)
        hdr = b"\x81"
        if n < 126:
            hdr += bytes([0x80 | n])
        elif n < 65536:
            hdr += bytes([0x80 | 126]) + struct.pack(">H", n)
        else:
            hdr += bytes([0x80 | 127]) + struct.pack(">Q", n)
        self.sock.sendall(hdr + mask + masked)

    def recv(self):
        b0, b1 = self._recv(2)
        opcode = b0 & 0x0F
        length = b1 & 0x7F
        if length == 126:
            length = struct.unpack(">H", self._recv(2))[0]
        elif length == 127:
            length = struct.unpack(">Q", self._recv(8))[0]
        data = self._recv(length)
        if opcode == 0x8:
            raise EOFError("closed")
        if opcode == 0x9:  # ping -> pong
            self.sock.sendall(b"\x8a\x80" + os.urandom(4))
            return self.recv()
        return data.decode("utf-8", "replace")


class CDP:
    def __init__(self, ws_url):
        self.ws = WS(ws_url)
        self.id = 0

    def call(self, method, **params):
        self.id += 1
        mid = self.id
        self.ws.send(json.dumps({"id": mid, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == mid:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})

    def evaluate(self, expression, await_promise=False):
        r = self.call(
            "Runtime.evaluate",
            expression=expression,
            returnByValue=True,
            awaitPromise=await_promise,
        )
        if "exceptionDetails" in r:
            raise RuntimeError(f"JS error: {r['exceptionDetails']}")
        return r.get("result", {}).get("value")


# --------------------------------------------------------------------------
# Chrome lifecycle
# --------------------------------------------------------------------------
def find_chrome():
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        p = subprocess.run(["which", name], capture_output=True, text=True)
        if p.returncode == 0:
            return p.stdout.strip()
    return None


class Chrome:
    def __init__(self, port=9222, profile="/tmp/cdp-render-profile"):
        self.binary = find_chrome()
        if not self.binary:
            raise RuntimeError("No Chrome binary found on PATH")
        self.port = port
        self.proc = subprocess.Popen(
            [
                self.binary, "--headless=new", "--disable-gpu", "--no-sandbox",
                "--hide-scrollbars", "--disable-dev-shm-usage",
                f"--remote-debugging-port={port}",
                f"--user-data-dir={profile}",
                "about:blank",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        self.cdp = None
        self._wait_for_devtools()
        self._connect()

    def _wait_for_devtools(self, timeout=30):
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                urllib.request.urlopen(
                    f"http://127.0.0.1:{self.port}/json/version", timeout=1
                ).read()
                return
            except Exception:
                time.sleep(0.25)
        raise RuntimeError("Chrome DevTools endpoint never came up")

    def _connect(self):
        targets = json.loads(
            urllib.request.urlopen(
                f"http://127.0.0.1:{self.port}/json/list", timeout=5
            ).read()
        )
        page = next(t for t in targets if t["type"] == "page")
        self.cdp = CDP(page["webSocketDebuggerUrl"])
        self.cdp.call("Page.enable")

    def close(self):
        self.proc.terminate()
        try:
            self.proc.wait(timeout=10)
        except Exception:
            self.proc.kill()


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------
# Wait for fonts before measuring, so layout height is correct.
READY_JS = """
(async () => {
  if (document.fonts && document.fonts.ready) { await document.fonts.ready; }
  return document.documentElement.scrollHeight;
})()
"""


def render_page(chrome, url, out_path, width, height, scale=2, mobile=False):
    cdp = chrome.cdp
    cdp.call(
        "Emulation.setDeviceMetricsOverride",
        width=width, height=height,
        deviceScaleFactor=scale, mobile=mobile,
    )
    cdp.call("Page.navigate", url=url)
    time.sleep(1.0)
    full = int(cdp.evaluate(READY_JS, await_promise=True) or height)
    full = min(full + 1, 30000)
    cdp.call(
        "Emulation.setDeviceMetricsOverride",
        width=width, height=full,
        deviceScaleFactor=scale, mobile=mobile,
    )
    time.sleep(0.4)
    shot = cdp.call(
        "Page.captureScreenshot", format="png", captureBeyondViewport=True
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(base64.b64decode(shot["data"]))
    return width, full


def parse_viewport(spec):
    name, _, dims = spec.partition(":")
    w, _, h = dims.partition("x")
    return name, int(w), int(h)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", help="HTML file or directory of HTML files")
    ap.add_argument("--out", default="./screenshots", help="output directory")
    ap.add_argument(
        "--viewport", action="append", default=[],
        help="name:WIDTHxHEIGHT (repeatable). Default: desktop:1440x1000 mobile:390x844",
    )
    ap.add_argument("--scale", type=int, default=2, help="device scale factor (default 2)")
    args = ap.parse_args()

    target = pathlib.Path(args.target).resolve()
    if target.is_dir():
        files = sorted(target.glob("*.html"))
    else:
        files = [target]
    if not files:
        print("No HTML files found", file=sys.stderr)
        return 1

    viewports = (
        [parse_viewport(v) for v in args.viewport]
        if args.viewport else DEFAULT_VIEWPORTS
    )

    out_dir = pathlib.Path(args.out).resolve()
    chrome = Chrome()
    try:
        for f in files:
            url = f.as_uri()
            for name, w, h in viewports:
                dest = out_dir / f"{f.stem}-{name}.png"
                rw, rh = render_page(
                    chrome, url, dest, w, h, args.scale, mobile=(name == "mobile")
                )
                print(
                    f"  {dest.name}  {rw}x{rh} @{args.scale}x  "
                    f"{dest.stat().st_size // 1024}KB"
                )
    finally:
        chrome.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
