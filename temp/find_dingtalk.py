#!/usr/bin/env python3
import urllib.request, json

url = "https://gitee.com/api/v5/repos/nashaofu/dingtalk/releases?per_page=3"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=20) as r:
    data = json.loads(r.read())

for release in data[:3]:
    print(f"版本: {release['tag_name']}")
    for a in release.get("assets", []):
        if ".deb" in a.get("name", ""):
            print(f"  deb: {a['browser_download_url']}")
    print()
