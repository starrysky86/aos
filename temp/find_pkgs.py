#!/usr/bin/env python3
"""Search pkgs.org for dingtalk deb package"""
import urllib.request, re

search_url = "https://www.pkgs.org/search/?q=dingtalk&type=deb"
req = urllib.request.Request(search_url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req, timeout=15) as r:
        html = r.read().decode("utf-8", errors="ignore")
    
    # Find .deb download links
    deb_links = re.findall(r'href="([^"]*\.deb[^"]*)"', html)
    if deb_links:
        print("Found .deb links:")
        for link in deb_links[:5]:
            print(f"  {link}")
    else:
        print("No .deb links found")
        # Show search results summary
        titles = re.findall(r'<a[^>]*title="([^"]+dingtalk[^"]+)"', html, re.IGNORECASE)
        for t in titles[:5]:
            print(f"  Found: {t}")
except Exception as e:
    print(f"Error: {e}")
