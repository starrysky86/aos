#!/usr/bin/env python3
import subprocess, re

packages = [
    "cinnamon", "cinnamon-core", "nemo", "muffin", "cjs",
    "cinnamon-desktop-data", "cinnamon-session", "cinnamon-settings-daemon",
    "libcinnamon-desktop4t64"
]

result = subprocess.run(
    ["apt-cache", "show"] + packages,
    capture_output=True, text=True, timeout=20
)

pkg_sizes = {}
for block in result.stdout.split("Package: "):
    if not block.strip():
        continue
    lines = block.split("\n")
    name = lines[0].strip()
    size_line = [l for l in lines if l.startswith("Installed-Size:")]
    if size_line and name:
        size_kb = int(size_line[0].split(":")[1].strip())
        pkg_sizes[name] = size_kb

total = sum(pkg_sizes.values())
print(f"Cinnamon 关键包总安装大小: {total/1024:.1f} MB\n")
for name, size_kb in sorted(pkg_sizes.items(), key=lambda x: -x[1]):
    print(f"  {size_kb/1024:6.1f} MB  {name}")
print(f"\n  {'总计':>8}  {total/1024:.1f} MB")
