#!/usr/bin/env python3
"""Test which GitHub hosts are reachable"""
import urllib.request, socket

targets = [
    ("api.github.com", 443),
    ("objects.githubusercontent.com", 443),
    ("codeload.github.com", 443),
    ("github.com", 443),
    ("raw.githubusercontent.com", 443),
    ("pipelines.actions.githubusercontent.com", 443),
]

for host, port in targets:
    print(f"\nTesting {host}:{port}...", end=" ", flush=True)
    try:
        sock = socket.create_connection((host, port), timeout=10)
        sock.close()
        print("OK")
    except Exception as e:
        print(f"FAIL: {e}")

# Also test a small file download via urllib
print("\nTrying small file download from raw.githubusercontent.com...")
url = "https://raw.githubusercontent.com/nashaofu/dingtalk/master/package.json"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req, timeout=15) as r:
        data = r.read(500)
        print(f"Success! Read {len(data)} bytes")
except Exception as e:
    print(f"Failed: {e}")
