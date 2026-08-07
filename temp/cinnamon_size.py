#!/usr/bin/env python3
import subprocess, re

# Get installed size of cinnamon family packages
result = subprocess.run(
    ["dpkg-query", "-Wf", "${Installed-Size} ${Package}\n"],
    capture_output=True, text=True
)

total = 0
cinnamon_pkgs = []
for line in result.stdout.strip().split("\n"):
    if not line.strip():
        continue
    parts = line.split(" ", 1)
    if len(parts) < 2:
        continue
    size_kb = int(parts[0])
    name = parts[1]
    if "cinnamon" in name or "muffin" in name or "nemo" in name or "cjs" in name:
        cinnamon_pkgs.append((size_kb, name))
        total += size_kb

print(f"Cinnamon 家族总安装大小: {total/1024:.1f} MB\n")
for s, n in sorted(cinnamon_pkgs, reverse=True):
    print(f"  {s/1024:.1f} MB  {n}")
