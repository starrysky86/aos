#!/usr/bin/env python3
import urllib.request, re, sys

# Try Gitee releases page
url = "https://gitee.com/nashaofu/dingtalk/releases"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req, timeout=20) as r:
        html = r.read().decode("utf-8", errors="ignore")
    # Find .deb links
    deb_links = re.findall(r'href="(https?://[^"]*\.deb[^"]*)"', html)
    if deb_links:
        print("Found .deb links:")
        for link in deb_links[:5]:
            print(f"  {link}")
    else:
        print("No .deb links found in HTML")
        # Try finding any download href
        dl_links = re.findall(r'href="([^"]*download[^"]*)"', html, re.IGNORECASE)
        print("Download links:", dl_links[:5])
except Exception as e:
    print(f"Error: {e}")
