#!/usr/bin/env python3
import urllib.request, json

url = "https://api.github.com/repos/nashaofu/dingtalk/releases/latest"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=15) as r:
    data = json.loads(r.read())

print("版本:", data.get("tag_name", ""))
print("预编译二进制:")
for a in data.get("assets", []):
    name = a["name"]
    url2 = a["browser_download_url"]
    size = a.get("size", 0)
    size_mb = size / 1024 / 1024
    print(f"  {name}  ({size_mb:.1f}MB)")
    print(f"    URL: {url2}")
