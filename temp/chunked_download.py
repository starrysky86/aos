#!/usr/bin/env python3
"""Chunked download of dingtalk deb using Range requests"""
import urllib.request, os, sys, time

URL = "https://github.com/nashaofu/dingtalk/releases/download/v2.1.22/dingtalk-2.1.22-latest-amd64.deb"
OUT_DIR = "/mnt/c/Users/chenlang/.qclaw/workspace-xiaolin/packages"
CHUNK = 2 * 1024 * 1024  # 2MB per chunk
HEADERS = {"User-Agent": "Mozilla/5.0"}

os.makedirs(OUT_DIR, exist_ok=True)

print(f"Starting chunked download: {URL}")
print(f"Output: {OUT_DIR}")

# First, get total size
print("\nFetching file size...")
req = urllib.request.Request(URL, headers=HEADERS)
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        total_size = int(r.headers.get("Content-Length", 0))
        print(f"Total size: {total_size / 1024 / 1024:.1f} MB")
except Exception as e:
    print(f"Error getting size: {e}")
    total_size = 60751872  # known size from API

# Calculate chunks
num_chunks = (total_size + CHUNK - 1) // CHUNK
print(f"Number of chunks: {num_chunks}")

manifest_path = os.path.join(OUT_DIR, "download_manifest.txt")
manifest = []
failed = []

for i in range(num_chunks):
    start = i * CHUNK
    end = min(start + CHUNK - 1, total_size - 1)
    chunk_file = os.path.join(OUT_DIR, f"chunk_{i:03d}")
    
    # Skip if already downloaded
    if os.path.exists(chunk_file):
        size = os.path.getsize(chunk_file)
        if size > 0:
            manifest.append((i, chunk_file, size))
            print(f"Chunk {i+1}/{num_chunks}: already exists ({size} bytes), skipping")
            continue
    
    print(f"Chunk {i+1}/{num_chunks} ({start:,}-{end:,}): ", end="", flush=True)
    range_req = urllib.request.Request(
        URL,
        headers={**HEADERS, "Range": f"bytes={start}-{end}"}
    )
    
    try:
        with urllib.request.urlopen(range_req, timeout=90) as r:
            data = r.read()
            with open(chunk_file, "wb") as f:
                f.write(data)
            size = len(data)
            manifest.append((i, chunk_file, size))
            elapsed = 0.1  # approximate
            speed = size / elapsed / 1024
            print(f"OK {size:,} bytes")
    except Exception as e:
        print(f"FAIL: {e}")
        failed.append(i)
    
    time.sleep(0.1)  # be polite

# Write manifest
with open(manifest_path, "w") as f:
    for i, path, size in manifest:
        f.write(f"{i},{path},{size}\n")

print(f"\n=== Download complete ===")
print(f"Successful: {len(manifest)}/{num_chunks}")
print(f"Failed chunks: {failed}")
print(f"Manifest: {manifest_path}")

# Try to assemble
if not failed and len(manifest) == num_chunks:
    out_file = os.path.join(OUT_DIR, "dingtalk-2.1.22-amd64.deb")
    print(f"\nAssembling final file...")
    with open(out_file, "wb") as out:
        for i, path, size in sorted(manifest):
            with open(path, "rb") as inp:
                out.write(inp.read())
    final_size = os.path.getsize(out_file)
    print(f"Final file: {out_file} ({final_size / 1024 / 1024:.1f} MB)")
else:
    print(f"\nCannot assemble: {len(failed)} chunks failed")
