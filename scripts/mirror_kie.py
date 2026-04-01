#!/usr/bin/env python3
"""
KIE Blog HTML Mirror
Phase 1 (replacement): uses WordPress REST API to enumerate all post URLs,
then downloads each post's HTML page into kie-mirror/blog.kie.org/YYYY/MM/slug.html.

Usage:
    python3 scripts/mirror_kie.py [--limit N] [--resume]
"""
import argparse
import json
import sys
import time
import random
from pathlib import Path
from urllib.parse import urlparse

import requests

API_BASE = "https://blog.kie.org/wp-json/wp/v2/posts"
MIRROR_ROOT = Path("kie-mirror/blog.kie.org")
STATE_FILE = Path("kie-mirror/.mirror_state.json")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; KIE-Archive/1.0)",
}


def load_mirror_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"downloaded": [], "failed": []}


def save_mirror_state(state: dict) -> None:
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2))
    tmp.rename(STATE_FILE)


def collect_all_post_urls(session: requests.Session, limit: int = 0) -> list[str]:
    """Paginate through WP REST API and collect all post link URLs."""
    urls = []
    page = 1
    per_page = 100

    while True:
        params = {"per_page": per_page, "page": page, "status": "publish", "_fields": "link"}
        resp = session.get(API_BASE, params=params, headers=HEADERS, timeout=30)

        if resp.status_code == 400:
            # WordPress returns 400 when page is out of range
            break
        if resp.status_code != 200:
            print(f"  API error page {page}: HTTP {resp.status_code}", file=sys.stderr)
            break

        posts = resp.json()
        if not posts:
            break

        batch_urls = [p["link"] for p in posts if p.get("link")]
        urls.extend(batch_urls)
        print(f"  Collected page {page}: {len(batch_urls)} posts (total so far: {len(urls)})")

        # Check X-WP-TotalPages header to know when to stop
        total_pages = int(resp.headers.get("X-WP-TotalPages", 0))
        if total_pages and page >= total_pages:
            break
        if len(posts) < per_page:
            break

        page += 1
        time.sleep(0.5)

        if limit and len(urls) >= limit:
            urls = urls[:limit]
            break

    return urls


def url_to_mirror_path(url: str) -> Path:
    """Convert a post URL to its local mirror path."""
    parsed = urlparse(url)
    # path is like /2023/07/post-slug.html
    rel = parsed.path.lstrip("/")
    return MIRROR_ROOT / rel


def download_post_html(url: str, session: requests.Session) -> str | None:
    """Download a post HTML page. Returns HTML string or None on failure."""
    for attempt in range(3):
        try:
            resp = session.get(url, headers=HEADERS, timeout=30)
            if resp.status_code == 200:
                return resp.text
            print(f"  HTTP {resp.status_code}: {url}")
            return None
        except requests.RequestException as e:
            if attempt < 2:
                time.sleep(2)
            else:
                print(f"  Failed after 3 attempts: {url} — {e}")
                return None
    return None


def main():
    parser = argparse.ArgumentParser(description="Mirror KIE blog HTML pages via REST API")
    parser.add_argument("--limit", type=int, default=0, help="Max posts to download (0=all)")
    parser.add_argument("--resume", action="store_true", help="Skip already-downloaded URLs")
    args = parser.parse_args()

    MIRROR_ROOT.mkdir(parents=True, exist_ok=True)
    state = load_mirror_state()

    session = requests.Session()

    print("Step 1: Collecting all post URLs via WordPress REST API...")
    all_urls = collect_all_post_urls(session, limit=args.limit)
    print(f"Found {len(all_urls)} post URLs total.\n")

    if args.resume:
        already_done = set(state["downloaded"])
        pending = [u for u in all_urls if u not in already_done]
        print(f"Resuming: {len(already_done)} already downloaded, {len(pending)} remaining.")
    else:
        pending = all_urls

    print(f"\nStep 2: Downloading {len(pending)} post HTML pages...")
    downloaded = 0
    failed = 0

    for i, url in enumerate(pending, 1):
        mirror_path = url_to_mirror_path(url)

        if mirror_path.exists() and args.resume:
            state["downloaded"].append(url)
            continue

        html = download_post_html(url, session)
        if html:
            mirror_path.parent.mkdir(parents=True, exist_ok=True)
            mirror_path.write_text(html, encoding="utf-8", errors="replace")
            state["downloaded"].append(url)
            downloaded += 1
        else:
            state["failed"].append(url)
            failed += 1

        if i % 50 == 0:
            save_mirror_state(state)
            print(f"  Progress: {i}/{len(pending)} — {downloaded} saved, {failed} failed")

        # Polite delay: 0.5–1.5s between requests
        time.sleep(0.5 + random.random())

    save_mirror_state(state)

    print(f"\nDone. Downloaded: {downloaded}, Failed: {failed}")
    print(f"Mirror at: {MIRROR_ROOT}")
    total_files = sum(1 for _ in MIRROR_ROOT.rglob("*.html"))
    print(f"Total HTML files in mirror: {total_files}")


if __name__ == "__main__":
    main()
