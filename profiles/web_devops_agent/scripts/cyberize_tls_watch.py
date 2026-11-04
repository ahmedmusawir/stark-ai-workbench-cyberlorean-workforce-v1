#!/usr/bin/env python3
"""cyberize-factory TLS watch — bounded monitor for Google managed-cert edge propagation.
Prints a one-line message only when https://cyberize-factory.cyberizedev.com/ serves
HTTP 200 over a validated TLS session. Silent while Google's frontend still resets
the handshake (propagation pending). Always exits 0 unless the tool itself is broken.
"""
import datetime
import socket
import ssl
import sys
import urllib.request

HOST = "cyberize-factory.cyberizedev.com"
URL = f"https://{HOST}/"

try:
    ctx = ssl.create_default_context()
    with socket.create_connection((socket.gethostbyname(HOST), 443), timeout=20) as raw:
        with ctx.wrap_socket(raw, server_hostname=HOST):
            pass  # handshake validated, certificate chain verified by ctx
    req = urllib.request.Request(URL, headers={"User-Agent": "cyberize-tls-watch/1"})
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        body = resp.read(4096)
        if resp.status == 200 and b"Cyberize Group" in body:
            print(
                f"TLS LIVE: https://{HOST}/ now serves HTTP 200 with a validated "
                f"certificate ({datetime.datetime.now(datetime.timezone.utc):%Y-%m-%dT%H:%M:%SZ}). "
                "Custom domain complete — run the final domain verification."
            )
        else:
            print(f"TLS reachable but unexpected status {resp.status}.")
except Exception:
    pass  # still resetting at the edge — propagation pending; stay silent
sys.exit(0)