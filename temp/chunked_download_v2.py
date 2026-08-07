#!/usr/bin/env python3
"""
Robust chunked download with retry + resume.
Handles GitHub CDN connection drops gracefully.
"""
import urllib.request, os, sys, time, socket

URL = "https://github.com/nashaofu/dingtalk/releases/download/v2.1.22/dingtalk-2.1.22-latest-amd64.deb"
OUT_DIR = "/mnt/c/Users/chenlang/.qclaw/workspace-xiaolin/packages"
CHUNK = 2 * 1024 * 1024  # 2MB per chunk
MAX_RETRIES = 5
TIMEOUT = 120
TOTAL_SIZE = 60751872  # known from API

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

os.makedirs(OUT_DIR, exist_ok=True)
num_chunks = (TOTAL_SIZE + CHUNK - 1) // CHUNK

def download_chunk(chunk_idx):
    """Download one chunk with retries. Returns (success, size)."""
    start = chunk_idx * CHUNK
    end = min(start + CHUNK - 1, TOTAL_SIZE - 1)
    chunk_file = os.path.join(OUT_DIR, f"chunk_{chunk_idx:03d}")
    
    # Skip if already good
    if os.path.exists(chunk_file) and os.path.getsize(chunk_file) > 1024:
        return True, os.path.getsize(chunk_file)
    
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            req = urllib.request.Request(
                URL,
                headers={**HEADERS, "Range": f"bytes={start}-{end}"}
            )
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                data = r.read()
                with open(chunk_file + ".tmp", "wb") as f:
                    f.write(data)
                os.rename(chunk_file + ".tmp", chunk_file)
                return True, len(data)
        except Exception as e:
            err = str(e)[:60]
            if attempt < MAX_RETRIES:
                wait = attempt * 3
                print(f"  FAIL (attempt {attempt}/{MAX_RETRIES}): {err}, retry in {wait}s...")
                time.sleep(wait)
            else:
                print(f"  GIVE UP after {MAX_RETRIES} attempts: {err}")
                return False, 0
    return False, 0

print(f"Chunked download: {URL}")
print(f"Total: {num_chunks} chunks x {CHUNK//1024}KB = {TOTAL_SIZE//1024//1024}MB\n")

# Check what's already downloaded
existing = []
for i in range(num_chunks):
    cf = os.path.join(OUT_DIR, f"chunk_{i:03d}")
    if os.path.exists(cf):
        existing.append(i)

print(f"Already downloaded: {len(existing)}/{num_chunks} chunks")
if existing:
    print(f"  Missing: {', '.join(str(i) for i in range(num_chunks) if i not in existing)}")

success = 0
failed_chunks = []

for i in range(num_chunks):
    print(f"Chunk {i+1:02d}/{num_chunks} ({i*CHUNK//1024}-{(i+1)*CHUNK//1024}KB): ", end="", flush=True)
    ok, size = download_chunk(i)
    if ok:
        success += 1
        speed = size / 60 / 1024  # rough KB/s
        print(f"OK {size//1024}KB")
    else:
        failed_chunks.append(i)
        print(f"FAILED")
    time.sleep(0.3)  # be polite

print(f"\n=== Result: {success}/{num_chunks} chunks successful ===")
if failed_chunks:
    print(f"Failed chunks: {failed_chunks}")

# Assemble if all done
if not failed_chunks and success == num_chunks:
    out_file = os.path.join(OUT_DIR, "dingtalk-2.1.22-amd64.deb")
    print(f"\nAssembling {out_file}...")
    with open(out_file, "wb") as out:
        for i in range(num_chunks):
            with open(os.path.join(OUT_DIR, f"chunk_{i:03d}"), "rb") as inp:
                out.write(inp.read())
    final_size = os.path.getsize(out_file)
    print(f"Done! Final: {final_size//1024//1024}MB ({final_size:,} bytes)")
    # Cleanup chunks
    for i in range(num_chunks):
        os.remove(os.path.join(OUT_DIR, f"chunk_{i:03d}"))
    print("Chunks cleaned up.")
else:
    print(f"\nIncomplete download ({success}/{num_chunks}). Run again to resume.")
    print("Already-downloaded chunks will be skipped.")
