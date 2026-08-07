#!/usr/bin/env python3
"""Test GitHub download mirror speeds"""
import urllib.request, time

GITHUB_DEB = "https://github.com/nashaofu/dingtalk/releases/download/v2.1.22/dingtalk-2.1.22-latest-amd64.deb"

mirrors = [
    ("Direct GitHub", GITHUB_DEB),
    ("ghproxy", "https://ghproxy.com/" + GITHUB_DEB),
    ("gitclone", "https://gitclone.com/github.com" + "/nashaofu/dingtalk/releases/download/v2.1.22/dingtalk-2.1.22-latest-amd64.deb"),
    ("hub.fastgit.xyz", GITHUB_DEB.replace("github.com", "hub.fastgit.xyz")),
    ("download.fastgit.org", GITHUB_DEB.replace("github.com", "download.fastgit.org")),
]

for name, url in mirrors:
    print(f"\nTesting {name}...")
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
        start = time.time()
        with urllib.request.urlopen(req, timeout=10) as r:
            elapsed = time.time() - start
            size = r.headers.get("Content-Length", "unknown")
            print(f"  Status: {r.status} | Time: {elapsed:.2f}s | Size: {size}")
    except Exception as e:
        print(f"  Error: {e}")
