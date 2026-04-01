#!/usr/bin/env python3
"""
Comprehensive image recovery — tries 5 approaches in sequence for each
remaining data: placeholder image in the archive.

Approach 1: data-src from kie-mirror/ (local, no network needed)
Approach 2: Multiple Wayback Machine timestamps via CDX API
Approach 3: archive.today (independent archive)
Approach 4: Cross-post sources (developers.redhat.com, DZone, Medium)
Approach 5: Bing/Google image search by filename (report only)

Usage:
    python3 scripts/recover_all.py [--limit N] [--approach 1,2,3,4]
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
MIRROR_ROOT = Path("kie-mirror/blog.kie.org")
STATE_PATH = Path("._state.json")

# Cross-post sources to check (site prefix + search URL pattern)
CROSS_POST_SOURCES = [
    "https://developers.redhat.com",
    "https://www.dzone.com",
    "https://medium.com",
]

WAYBACK_CDX = "https://web.archive.org/cdx/search/cdx"
ARCHIVE_TODAY = "https://archive.ph"


# ─── Helpers ──────────────────────────────────────────────────────────────────

def save_image(content: bytes, original_url: str, post_date: str, state: dict) -> str:
    """Hash, deduplicate, save image. Returns local relative path."""
    content_hash = lib.compute_image_hash(content)
    if content_hash in state["image_cache"]:
        return state["image_cache"][content_hash]
    local_rel = lib.get_local_image_path(original_url, content_hash, post_date)
    abs_path = LEGACY_DIR / "assets" / local_rel
    abs_path.parent.mkdir(parents=True, exist_ok=True)
    abs_path.write_bytes(content)
    state["image_cache"][content_hash] = local_rel
    return local_rel


def wire_image(post_path: Path, img_tag, local_rel: str, noscript_sib=None) -> None:
    """Update img src to local path and remove noscript sibling if present."""
    img_tag["src"] = f"../../assets/{local_rel}"
    if noscript_sib:
        noscript_sib.decompose()


# ─── Approach 1: data-src from kie-mirror ─────────────────────────────────────

def try_datasrc(img_tag, mirror_soup, session: requests.Session, state: dict, post_date: str) -> bytes | None:
    """
    Find the corresponding img in the mirror HTML by position and extract data-src.
    Returns downloaded content or None.
    """
    if not mirror_soup:
        return None

    # Find ALL imgs with data-src in the mirror
    mirror_imgs = [i for i in mirror_soup.find_all("img") if i.get("data-src")]
    legacy_data_imgs = []  # will be filled by caller context

    # Try to get data-src by matching alt text first, then position
    alt = img_tag.get("alt", "")
    for m_img in mirror_imgs:
        if alt and m_img.get("alt", "") == alt:
            datasrc = m_img["data-src"]
            content = lib.download_image(datasrc, session)
            if content:
                return content, datasrc

    return None


def get_all_datasrc_urls(mirror_soup) -> list[str]:
    """Extract all data-src URLs from a mirror HTML soup."""
    if not mirror_soup:
        return []
    urls = []
    for img in mirror_soup.find_all("img"):
        ds = img.get("data-src", "")
        if ds and ds.startswith("http"):
            urls.append(ds)
    return urls


# ─── Approach 2: Wayback CDX (multiple timestamps) ───────────────────────────

def try_wayback_cdx(original_url: str, session: requests.Session) -> bytes | None:
    """Try multiple Wayback snapshots via CDX API."""
    try:
        resp = session.get(WAYBACK_CDX, params={
            "url": original_url, "output": "json",
            "fl": "timestamp,statuscode", "filter": "statuscode:200",
            "limit": "5", "fl": "timestamp",
        }, timeout=15)
        if resp.status_code != 200:
            return None
        rows = resp.json()
        if not rows or len(rows) < 2:  # first row is header
            return None
        for row in rows[1:]:
            ts = row[0]
            wb_url = f"https://web.archive.org/web/{ts}if_/{original_url}"
            content = lib.download_image(wb_url, session)
            if content and len(content) > 500:
                return content
    except Exception:
        pass
    return None


# ─── Approach 3: archive.today ────────────────────────────────────────────────

def try_archive_today(original_url: str, session: requests.Session) -> bytes | None:
    """Try to fetch an image from archive.today."""
    try:
        check_url = f"{ARCHIVE_TODAY}/{original_url}"
        resp = session.get(check_url, timeout=15, allow_redirects=True)
        if resp.status_code == 200 and resp.headers.get("content-type", "").startswith("image/"):
            return resp.content
    except Exception:
        pass
    return None


# ─── Approach 4: Cross-post sources ──────────────────────────────────────────

def try_cross_posts(original_post_url: str, img_filename: str,
                    session: requests.Session) -> bytes | None:
    """
    Search developers.redhat.com and DZone for the same post, then look
    for an image with the same filename.
    """
    slug = original_post_url.rstrip("/").split("/")[-1].replace(".html", "")

    for base in CROSS_POST_SOURCES:
        try:
            # Try a predictable URL pattern
            for pattern in [
                f"{base}/blog/{slug}",
                f"{base}/articles/{slug}",
                f"{base}/{slug}",
            ]:
                resp = session.get(pattern, timeout=15, allow_redirects=True)
                if resp.status_code != 200:
                    continue
                soup = BeautifulSoup(resp.text, "lxml")
                # Look for an image with the same filename
                for img in soup.find_all("img", src=True):
                    src = img["src"]
                    if img_filename.lower() in src.lower():
                        full_url = src if src.startswith("http") else base + src
                        content = lib.download_image(full_url, session)
                        if content:
                            return content
        except Exception:
            continue
    return None


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Comprehensive image recovery — all 5 approaches")
    parser.add_argument("--limit", type=int, default=0, help="Max posts to process (0=all)")
    parser.add_argument("--approaches", default="1,2,3,4", help="Approaches to try (comma-separated)")
    args = parser.parse_args()

    approaches = set(int(a) for a in args.approaches.split(","))
    state = lib.load_state(STATE_PATH)

    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (compatible; KIE-Archive-Recovery/1.0)"

    print("Scanning for remaining data: placeholder images...")
    posts_to_fix: list[dict] = []

    for html_path in sorted((LEGACY_DIR / "posts").rglob("*.html")):
        soup = BeautifulSoup(html_path.read_text(errors="replace"), "lxml")
        data_imgs = [img for img in soup.find_all("img")
                     if (img.get("src") or "").startswith("data:")]
        if not data_imgs:
            continue

        sidecar = html_path.with_suffix(".json")
        meta = {}
        if sidecar.exists():
            try:
                meta = json.loads(sidecar.read_text())
            except Exception:
                pass

        orig_url = meta.get("original_url", "")
        post_date = meta.get("date", "2000-01-01")

        # Find mirror file
        mirror_file = None
        mirror_soup = None
        if orig_url:
            path = urlparse(orig_url).path.strip("/")
            mf = MIRROR_ROOT / path
            if mf.exists() and mf.is_file():
                mirror_file = mf
                try:
                    mirror_soup = BeautifulSoup(mf.read_text(errors="replace"), "lxml")
                except Exception:
                    pass

        posts_to_fix.append({
            "html_path": html_path,
            "soup": soup,
            "data_imgs": data_imgs,
            "orig_url": orig_url,
            "post_date": post_date,
            "mirror_soup": mirror_soup,
        })

    print(f"Found {len(posts_to_fix)} posts with {sum(len(p['data_imgs']) for p in posts_to_fix)} remaining placeholders")
    print(f"Running approaches: {sorted(approaches)}\n")

    if args.limit:
        posts_to_fix = posts_to_fix[:args.limit]

    stats = {1: 0, 2: 0, 3: 0, 4: 0, "failed": 0}

    for pi, post in enumerate(posts_to_fix, 1):
        html_path = post["html_path"]
        soup = post["soup"]
        mirror_soup = post["mirror_soup"]
        orig_url = post["orig_url"]
        post_date = post["post_date"]
        changed = False

        # Get all data-src URLs from mirror (Approach 1 source)
        mirror_datasrcs = get_all_datasrc_urls(mirror_soup) if mirror_soup else []

        print(f"[{pi}/{len(posts_to_fix)}] {html_path.name} ({len(post['data_imgs'])} placeholders, "
              f"{len(mirror_datasrcs)} mirror data-srcs)")

        # Re-fetch img list fresh (might have changed if multiple passes)
        data_imgs = [img for img in soup.find_all("img")
                     if (img.get("src") or "").startswith("data:")]

        # Match data: imgs to mirror data-srcs by position
        datasrc_queue = list(mirror_datasrcs)

        for img_idx, img in enumerate(data_imgs):
            content = None
            approach_used = None
            datasrc_url = datasrc_queue[img_idx] if img_idx < len(datasrc_queue) else None

            # Approach 1: data-src from mirror
            if 1 in approaches and datasrc_url:
                content = lib.download_image(datasrc_url, session)
                if content:
                    approach_used = 1
                    print(f"  [1] ✓ {datasrc_url.split('/')[-1][:50]}")

            # Approach 2: Wayback CDX (multiple timestamps)
            if not content and 2 in approaches and datasrc_url:
                content = try_wayback_cdx(datasrc_url, session)
                if content:
                    approach_used = 2
                    print(f"  [2] ✓ Wayback CDX: {datasrc_url.split('/')[-1][:50]}")
                time.sleep(0.3)

            # Approach 3: archive.today
            if not content and 3 in approaches and datasrc_url:
                content = try_archive_today(datasrc_url, session)
                if content:
                    approach_used = 3
                    print(f"  [3] ✓ archive.today: {datasrc_url.split('/')[-1][:50]}")

            # Approach 4: Cross-post sources
            if not content and 4 in approaches and datasrc_url:
                img_filename = datasrc_url.split("/")[-1].split("?")[0]
                content = try_cross_posts(orig_url, img_filename, session)
                if content:
                    approach_used = 4
                    print(f"  [4] ✓ Cross-post: {img_filename[:50]}")

            if content:
                local_rel = save_image(content, datasrc_url or "unknown", post_date, state)
                wire_image(html_path.parent / html_path.name, img, local_rel)
                # Actually wire it in the soup
                img["src"] = f"../../assets/{local_rel}"
                stats[approach_used] += 1
                changed = True
            else:
                if datasrc_url:
                    fname = datasrc_url.split("/")[-1].split("?")[0][:50]
                    print(f"  ✗ All approaches failed: {fname}")
                stats["failed"] += 1

            time.sleep(0.2)

        if changed:
            out = str(soup)
            if not out.startswith("<!DOCTYPE"):
                out = "<!DOCTYPE html>\n" + out
            html_path.write_text(out, encoding="utf-8")

        if pi % 50 == 0:
            lib.save_state(state, STATE_PATH)
            print(f"  Progress: {pi}/{len(posts_to_fix)}")

    lib.save_state(state, STATE_PATH)

    print(f"\n=== Summary ===")
    print(f"Approach 1 (data-src mirror):    {stats[1]}")
    print(f"Approach 2 (Wayback CDX):        {stats[2]}")
    print(f"Approach 3 (archive.today):      {stats[3]}")
    print(f"Approach 4 (cross-post sources): {stats[4]}")
    print(f"Failed all approaches:           {stats['failed']}")

    # Approach 5: report filenames for manual Yandex/Google search
    still_broken = []
    for post in posts_to_fix:
        soup = BeautifulSoup(post["html_path"].read_text(errors="replace"), "lxml")
        remaining = [img for img in soup.find_all("img")
                     if (img.get("src") or "").startswith("data:")]
        if remaining and post["mirror_soup"]:
            datasrcs = get_all_datasrc_urls(post["mirror_soup"])
            for ds in datasrcs:
                still_broken.append(ds)

    if still_broken:
        report = LEGACY_DIR / "unrecovered-images.txt"
        report.write_text("\n".join(still_broken))
        print(f"\nApproach 5 (manual): {len(still_broken)} URLs saved to {report}")
        print("Search these on Yandex/Google Images or Bing for manual recovery.")


if __name__ == "__main__":
    main()
