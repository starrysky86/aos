#!/usr/bin/env python3
"""Test dingtalk deb download with Range header"""
import urllib.request, sys

url = "https://github.com/nashaofu/dingtalk/releases/download/v2.1.22/dingtalk-2.1.22-latest-amd64.deb"

print(f"URL: {url}")
print(f"File size: 57.9MB")
print()

# First, follow redirects to find final URL
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

opener = urllib.request.build_opener(NoRedirect)
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

try:
    with opener.open(req, timeout=15) as r:
        final_url = r.url
        print(f"Final URL (after redirect): {final_url}")
        print(f"Status: {r.status}")
        print(f"Content-Length: {r.headers.get('Content-Length', 'unknown')}")
except Exception as e:
    print(f"Error: {e}")

print("\nTrying HEAD request to find CDN URL...")
try:
    head_req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(head_req, timeout=15) as r:
        print(f"Final URL: {r.url}")
        print(f"Status: {r.status}")
        print(f"Content-Length: {r.headers.get('Content-Length', 'unknown')}")
        # Try Range request
        range_req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0",
            "Range": "bytes=0-1048575"  # First 1MB
        })
        with urllib.request.urlopen(range_req, timeout=30) as r2:
            data = r2.read()
            print(f"\nRange 0-1MB: got {len(data)} bytes from {r2.url}")
except Exception as e:
    print(f"Error: {e}")
