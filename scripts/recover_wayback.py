#!/usr/bin/env python3
"""
Recover failed images from the Wayback Machine.
Scans legacy/posts/ for img tags with external URLs matching known-failed
image hosts, attempts Wayback Machine retrieval, saves locally, rewrites src.

Usage:
    python3 scripts/recover_wayback.py [--dry-run]
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).parent))
import kie_lib as lib

LEGACY_DIR = Path("legacy")
STATE_PATH = Path("._state.json")

# Domains we skip (Google user content — not archived reliably)
SKIP_DOMAINS = {
    'lh3.googleusercontent.com', 'lh4.googleusercontent.com',
    'lh5.googleusercontent.com', 'lh6.googleusercontent.com',
}

WAYBACK_AVAILABILITY = "https://archive.org/wayback/available"
WAYBACK_BASE = "https://web.archive.org/web"


def check_wayback(url: str, session: requests.Session) -> str | None:
    """Return Wayback Machine URL for the closest snapshot, or None."""
    try:
        resp = session.get(
            WAYBACK_AVAILABILITY,
            params={"url": url, "timestamp": "20231231"},
            timeout=15
        )
        if resp.status_code != 200:
            return None
        data = resp.json()
        snap = data.get("archived_snapshots", {}).get("closest", {})
        if snap.get("available") and snap.get("url"):
            return snap["url"]
        return None
    except Exception:
        return None


def download_from_wayback(wayback_url: str, session: requests.Session) -> bytes | None:
    """Download image bytes from a Wayback Machine URL."""
    try:
        resp = session.get(wayback_url, timeout=30)
        if resp.status_code == 200 and len(resp.content) > 500:
            return resp.content
        return None
    except Exception:
        return None


def find_posts_with_external_images(legacy_dir: Path, skip_domains: set) -> dict[str, list[Path]]:
    """
    Scan all post HTML files. Return mapping:
        original_image_url -> [list of post html Paths that reference it]
    Only includes URLs not in skip_domains and not already local (../../assets/).
    """
    url_to_posts: dict[str, list[Path]] = {}
    for post_path in (legacy_dir / "posts").rglob("*.html"):
        try:
            soup = BeautifulSoup(post_path.read_text(encoding='utf-8', errors='replace'), 'lxml')
        except Exception:
            continue
        for img in soup.find_all("img", src=True):
            src = img["src"]
            if src.startswith("../../assets/") or src.startswith("data:"):
                continue
            if not src.startswith("http"):
                continue
            domain = urlparse(src).netloc
            if domain in skip_domains:
                continue
            url_to_posts.setdefault(src, []).append(post_path)
    return url_to_posts


def rewrite_image_in_post(post_path: Path, old_url: str, new_local_path: str) -> bool:
    """Replace img src=old_url with new_local_path in the post HTML file."""
    try:
        html = post_path.read_text(encoding='utf-8', errors='replace')
        soup = BeautifulSoup(html, 'lxml')
        changed = False
        for img in soup.find_all("img", src=True):
            if img["src"] == old_url:
                img["src"] = new_local_path
                changed = True
        if changed:
            # Reconstruct — preserve doctype
            out = str(soup)
            if not out.startswith("<!DOCTYPE"):
                out = "<!DOCTYPE html>\n" + out
            post_path.write_text(out, encoding='utf-8')
        return changed
    except Exception as e:
        print(f"  ERROR rewriting {post_path.name}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Recover failed images from Wayback Machine")
    parser.add_argument("--dry-run", action="store_true", help="Check only, don't write files")
    args = parser.parse_args()

    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (compatible; KIE-Archive-Recovery/1.0)"

    state = lib.load_state(STATE_PATH)

    print("Scanning post HTML files for external image URLs...")
    url_to_posts = find_posts_with_external_images(LEGACY_DIR, SKIP_DOMAINS)
    print(f"Found {len(url_to_posts)} unique external image URLs across posts\n")

    recovered = 0
    not_found = 0
    skipped = 0

    for i, (img_url, posts) in enumerate(url_to_posts.items(), 1):
        print(f"[{i}/{len(url_to_posts)}] {img_url[:80]}")

        # Check Wayback Machine
        wayback_url = check_wayback(img_url, session)
        if not wayback_url:
            print(f"  ✗ Not in Wayback Machine")
            not_found += 1
            time.sleep(0.3)
            continue

        print(f"  ✓ Found: {wayback_url[:80]}")

        if args.dry_run:
            skipped += 1
            time.sleep(0.3)
            continue

        # Download
        content = download_from_wayback(wayback_url, session)
        if not content:
            print(f"  ✗ Download failed")
            not_found += 1
            time.sleep(0.3)
            continue

        # Save locally — use hash + original filename
        content_hash = lib.compute_image_hash(content)
        if content_hash in state["image_cache"]:
            local_rel = state["image_cache"][content_hash]
            print(f"  → Reusing cached: {local_rel}")
        else:
            # Use date from first post's sidecar for directory placement
            first_post = posts[0]
            sidecar = first_post.with_suffix(".json")
            post_date = "2000-01-01"
            if sidecar.exists():
                try:
                    meta = json.loads(sidecar.read_text())
                    post_date = meta.get("date", post_date)
                except Exception:
                    pass

            local_rel = lib.get_local_image_path(img_url, content_hash, post_date)
            abs_path = LEGACY_DIR / "assets" / local_rel
            abs_path.parent.mkdir(parents=True, exist_ok=True)
            abs_path.write_bytes(content)
            state["image_cache"][content_hash] = local_rel
            lib.save_state(state, STATE_PATH)
            print(f"  → Saved: {local_rel}")

        # Rewrite all posts that reference this URL
        rel_from_post = f"../../assets/{local_rel}"
        for post_path in posts:
            if rewrite_image_in_post(post_path, img_url, rel_from_post):
                print(f"    Updated: {post_path.name}")
        recovered += 1
        time.sleep(0.5)

    print(f"\n=== Summary ===")
    print(f"Recovered:    {recovered}")
    print(f"Not in WB:    {not_found}")
    if args.dry_run:
        print(f"Dry run:      {skipped}")
    print(f"Skipped (Google): {len([u for u in url_to_posts if urlparse(u).netloc in SKIP_DOMAINS])}")


if __name__ == "__main__":
    main()
