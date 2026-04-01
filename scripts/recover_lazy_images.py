#!/usr/bin/env python3
"""
Recover lazy-loaded images whose data-src was stripped during extraction.
These appear in the archive as 1x1 transparent GIFs but the real URL
survives in a <noscript> sibling tag.

Pattern:
  <img src="data:image/gif;base64,...">
  <noscript><img src="https://real-image-url.jpg"></noscript>

This script:
  1. Scans all posts for this pattern
  2. Downloads the real image from the noscript URL
  3. Saves it locally with hash-based dedup
  4. Replaces the data: img src with the local path
  5. Removes the now-redundant <noscript> sibling

Usage:
    python3 scripts/recover_lazy_images.py [--dry-run] [--limit N]
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).parent))
import kie_lib as lib

LEGACY_DIR = Path("legacy")
STATE_PATH = Path("._state.json")
NOSCRIPT_SRC_RE = re.compile(r'src=["\' ](https?://[^"\'>\s]+)["\' ]', re.IGNORECASE)
NOSCRIPT_LOCAL_RE = re.compile(r'src=["\'](\.\.\/[^"\']+)["\']', re.IGNORECASE)


def find_lazy_images(html_path: Path) -> list[tuple]:
    """
    Return list of (img_tag, real_url, post_date) for each lazy-loaded image.
    img_tag is the BeautifulSoup Tag for the data: placeholder img.
    """
    soup = BeautifulSoup(html_path.read_text(errors="replace"), "lxml")
    results = []

    # Get post date from sidecar for image path placement
    sidecar = html_path.with_suffix(".json")
    post_date = "2000-01-01"
    if sidecar.exists():
        try:
            meta = json.loads(sidecar.read_text())
            post_date = meta.get("date", post_date)
        except Exception:
            pass

    for img in soup.find_all("img"):
        try:
            src = img.get("src", "") or ""
        except Exception:
            continue
        if not src.startswith("data:"):
            continue
        next_sib = img.find_next_sibling()
        if not next_sib or next_sib.name != "noscript":
            continue
        noscript_text = str(next_sib)

        # Case 1: noscript already has a local path (downloaded during extraction)
        # Just copy it to the main img and remove the noscript.
        local_match = NOSCRIPT_LOCAL_RE.search(noscript_text)
        if local_match:
            results.append((soup, img, next_sib, local_match.group(1), post_date, html_path, "local"))
            continue

        # Case 2: noscript has an http URL — need to download it
        http_match = NOSCRIPT_SRC_RE.search(noscript_text)
        if http_match:
            results.append((soup, img, next_sib, http_match.group(1), post_date, html_path, "remote"))

    return results


def main():
    parser = argparse.ArgumentParser(description="Recover lazy-loaded images in archive")
    parser.add_argument("--dry-run", action="store_true", help="Report only, don't download")
    parser.add_argument("--limit", type=int, default=0, help="Max posts to process (0=all)")
    args = parser.parse_args()

    state = lib.load_state(STATE_PATH)
    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (compatible; KIE-Archive-Recovery/1.0)"

    # Scan all posts
    print("Scanning posts for lazy-loaded images...")
    posts_dir = LEGACY_DIR / "posts"
    all_lazy: list[dict] = []

    for html_path in sorted(posts_dir.rglob("*.html")):
        hits = find_lazy_images(html_path)
        if hits:
            soup = hits[0][0]
            all_lazy.append({
                "html_path": html_path,
                "soup": soup,
                "hits": [(img, ns, url, date, mode) for _, img, ns, url, date, _, mode in hits],
            })

    total_images = sum(len(p["hits"]) for p in all_lazy)
    print(f"Found {len(all_lazy)} posts with {total_images} lazy-loaded images\n")

    if args.dry_run:
        for p in all_lazy[:20]:
            print(f"  {p['html_path'].name}: {len(p['hits'])} image(s)")
            for _, _, url, _, mode in p["hits"][:2]:
                print(f"    [{mode}] {url[:80]}")
        return

    if args.limit:
        all_lazy = all_lazy[:args.limit]

    downloaded = 0
    failed = 0
    skipped = 0

    for i, post in enumerate(all_lazy, 1):
        html_path = post["html_path"]
        soup = post["soup"]
        hits = post["hits"]
        changed = False

        print(f"[{i}/{len(all_lazy)}] {html_path.name} ({len(hits)} image(s))")

        for img, noscript_tag, url, post_date, mode in hits:
            if mode == "local":
                # noscript already has a local path — just wire up the main img
                img["src"] = url
                noscript_tag.decompose()
                changed = True
                skipped += 1
                print(f"  → Wired local: {url}")
                continue

            # mode == "remote": download the image
            content = lib.download_image(url, session)
            if content is None:
                print(f"  ✗ Failed: {url[:70]}")
                failed += 1
                time.sleep(0.3)
                continue

            content_hash = lib.compute_image_hash(content)
            if content_hash in state["image_cache"]:
                local_rel = state["image_cache"][content_hash]
                print(f"  → Reusing cached: {local_rel}")
            else:
                local_rel = lib.get_local_image_path(url, content_hash, post_date)
                abs_path = LEGACY_DIR / "assets" / local_rel
                abs_path.parent.mkdir(parents=True, exist_ok=True)
                abs_path.write_bytes(content)
                state["image_cache"][content_hash] = local_rel
                fname = url.split("/")[-1].split("?")[0][:40]
                print(f"  ✓ Downloaded: {local_rel} ({fname})")
                downloaded += 1

            img["src"] = f"../../assets/{local_rel}"
            noscript_tag.decompose()
            changed = True
            time.sleep(0.2)

        if changed:
            # Write updated HTML back
            out = str(soup)
            if not out.startswith("<!DOCTYPE"):
                out = "<!DOCTYPE html>\n" + out
            html_path.write_text(out, encoding="utf-8")

        if i % 50 == 0:
            lib.save_state(state, STATE_PATH)
            print(f"  Progress: {i}/{len(all_lazy)} posts, {downloaded} downloaded, {failed} failed")

    lib.save_state(state, STATE_PATH)
    print(f"\n=== Summary ===")
    print(f"Posts processed:  {len(all_lazy)}")
    print(f"Images downloaded: {downloaded}")
    print(f"Images reused:    {skipped}")
    print(f"Failed:           {failed}")


if __name__ == "__main__":
    main()
