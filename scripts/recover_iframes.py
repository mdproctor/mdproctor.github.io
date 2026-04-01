#!/usr/bin/env python3
"""
Recover empty-src iframes using Playwright headless browser.
Visits each affected post on blog.kie.org, waits for JS to fill iframe srcs,
then updates the local archive HTML accordingly.

Usage:
    python3 scripts/recover_iframes.py [--limit N]
"""
import argparse
import json
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

sys.path.insert(0, str(Path(__file__).parent))
import kie_lib as lib

LEGACY_DIR = Path("legacy")
STATE_PATH = Path("._state.json")
IFRAME_POSTS = Path("/tmp/iframe_posts.json")


def get_live_iframe_srcs(page, original_url: str) -> list[str]:
    """
    Navigate to original_url, wait for JS, return list of non-empty iframe srcs.
    """
    try:
        page.goto(original_url, wait_until="networkidle", timeout=30000)
    except PlaywrightTimeout:
        try:
            page.goto(original_url, wait_until="domcontentloaded", timeout=20000)
            page.wait_for_timeout(3000)
        except Exception:
            return []
    except Exception:
        return []

    srcs = []
    try:
        iframes = page.query_selector_all("article iframe, .entry-content iframe")
        for iframe in iframes:
            src = iframe.get_attribute("src") or ""
            if src and src.strip():
                srcs.append(src.strip())
    except Exception:
        pass
    return srcs


def process_iframe_src(src: str, post_path: Path, state: dict, session: requests.Session) -> str | None:
    """
    Given a live iframe src, determine what to replace it with in the archive.
    Returns replacement HTML string, or None if unhandled.
    """
    video_id = lib.extract_youtube_id(src)
    if video_id:
        # YouTube — download thumbnail and create link
        thumb_dir = LEGACY_DIR / "assets" / "images" / "youtube"
        thumb_dir.mkdir(parents=True, exist_ok=True)
        thumb_path = thumb_dir / f"{video_id}.jpg"
        if not thumb_path.exists():
            for quality in ["hqdefault", "mqdefault", "default"]:
                thumb_url = f"https://img.youtube.com/vi/{video_id}/{quality}.jpg"
                content = lib.download_image(thumb_url, session)
                if content and len(content) > 1000:
                    thumb_path.write_bytes(content)
                    break
        thumb_local = f"../../assets/images/youtube/{video_id}.jpg"
        return lib.make_youtube_replacement(video_id, thumb_local)

    # Non-YouTube iframe — keep as live embed with a note
    domain = urlparse(src).netloc or src[:40]
    return (
        f'<figure class="embed-recovered">'
        f'<p class="archive-note">[Embedded from {domain} — requires internet: '
        f'<a href="{src}" target="_blank" rel="noopener">{src[:80]}</a>]</p>'
        f'<iframe src="{src}" loading="lazy" style="width:100%;min-height:400px;border:0"></iframe>'
        f'</figure>'
    )


def update_post_iframes(post_path: Path, live_srcs: list[str], state: dict, session: requests.Session) -> int:
    """
    Replace empty-src iframes in post_path with content based on live_srcs.
    Returns number of iframes updated.
    """
    html = post_path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(html, "lxml")

    empty_iframes = [f for f in soup.find_all("iframe") if not f.get("src", "").strip()]
    if not empty_iframes or not live_srcs:
        return 0

    updated = 0
    for iframe, src in zip(empty_iframes, live_srcs):
        replacement_html = process_iframe_src(src, post_path, state, session)
        if replacement_html:
            replacement = BeautifulSoup(replacement_html, "lxml").body.next
            iframe.replace_with(replacement)
            updated += 1

    if updated:
        out = str(soup)
        if not out.startswith("<!DOCTYPE"):
            out = "<!DOCTYPE html>\n" + out
        post_path.write_text(out, encoding="utf-8")

    return updated


def main():
    parser = argparse.ArgumentParser(description="Recover empty-src iframes via Playwright")
    parser.add_argument("--limit", type=int, default=0, help="Max posts to process (0=all)")
    args = parser.parse_args()

    if not IFRAME_POSTS.exists():
        print("ERROR: /tmp/iframe_posts.json not found. Run the scan first.")
        sys.exit(1)

    posts = json.loads(IFRAME_POSTS.read_text())
    if args.limit:
        posts = posts[:args.limit]

    state = lib.load_state(STATE_PATH)
    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (compatible; KIE-Archive-Recovery/1.0)"

    print(f"Processing {len(posts)} posts with empty-src iframes...\n")

    total_recovered = 0
    total_failed = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (compatible; KIE-Archive/1.0)"})

        for i, entry in enumerate(posts, 1):
            post_path = Path(entry["post"])
            original_url = entry["original_url"]
            expected_count = len(entry["iframes"])

            print(f"[{i}/{len(posts)}] {original_url}")

            if not original_url:
                print(f"  ✗ No original URL")
                total_failed += 1
                continue

            live_srcs = get_live_iframe_srcs(page, original_url)

            if not live_srcs:
                print(f"  ✗ No iframes found on live page (expected {expected_count})")
                total_failed += 1
                continue

            print(f"  Found {len(live_srcs)} live iframe src(s):")
            for s in live_srcs:
                print(f"    {s[:80]}")

            updated = update_post_iframes(post_path, live_srcs, state, session)
            if updated:
                print(f"  ✓ Updated {updated} iframe(s) in {post_path.name}")
                total_recovered += updated
            else:
                print(f"  ~ No matching empty iframes to update")

            time.sleep(0.5)

        browser.close()

    lib.save_state(state, STATE_PATH)

    print(f"\n=== Summary ===")
    print(f"Posts processed: {len(posts)}")
    print(f"Iframes recovered: {total_recovered}")
    print(f"Posts with no live iframes: {total_failed}")


if __name__ == "__main__":
    main()
