#!/usr/bin/env python3
"""
KIE Blog Archive Extractor
Phase 2: reads kie-mirror/, writes to legacy/

Usage:
    python scripts/extract_kie.py --mirror kie-mirror/blog.kie.org \
                                   --legacy legacy \
                                   --state ._state.json \
                                   [--limit 5]
"""
import argparse
import json
import re
import sys
import time
from datetime import date as _date
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).parent))
import kie_lib as lib

NEEDS_REVIEW = []


def process_images(article, post_date, state, legacy_dir, session):
    """Download article images, deduplicate, rewrite src to local paths."""
    image_records = []
    for img in article.find_all('img'):
        src = img.get('src', '')
        if not src or src.startswith('data:'):
            continue
        content = lib.download_image(src, session)
        if content is None:
            NEEDS_REVIEW.append({'type': 'image_download_failed', 'url': src})
            continue
        # MIME check via magic bytes (avoids deprecated imghdr / Python 3.13 removal)
        KNOWN_SIGS = {
            b'\xff\xd8\xff': 'jpeg', b'\x89PNG': 'png',
            b'GIF8': 'gif', b'RIFF': 'webp',
            b'<svg': 'svg', b'\x00\x00\x01\x00': 'ico',
        }
        detected = next((t for sig, t in KNOWN_SIGS.items() if content[:len(sig)] == sig), None)
        if detected not in ('jpeg', 'png', 'gif', 'webp', 'svg', None):
            NEEDS_REVIEW.append({'type': 'unusual_mime', 'url': src, 'detected': detected})

        content_hash = lib.compute_image_hash(content)
        if content_hash in state['image_cache']:
            local_rel = state['image_cache'][content_hash]
        else:
            local_rel = lib.get_local_image_path(src, content_hash, post_date)
            abs_path = legacy_dir / 'assets' / local_rel
            abs_path.parent.mkdir(parents=True, exist_ok=True)
            abs_path.write_bytes(content)
            state['image_cache'][content_hash] = local_rel

        # Rewrite src to relative path from post file (posts/author/file.html → ../../assets/...)
        img['src'] = f"../../assets/{local_rel}"
        image_records.append({'original_url': src, 'local_path': f"../../assets/{local_rel}", 'hash': content_hash})

    return image_records


def process_youtube(article, legacy_dir, session):
    """Replace YouTube iframes with thumbnail images + links."""
    video_records = []
    for iframe in article.find_all('iframe'):
        src = iframe.get('src', '')
        video_id = lib.extract_youtube_id(src)
        if video_id is None:
            # Non-YouTube iframe — flag for review
            domain = src.split('/')[2] if src.startswith('http') else 'unknown'
            NEEDS_REVIEW.append({'type': 'unknown_iframe', 'src': src, 'domain': domain})
            note = BeautifulSoup(
                f'<figure class="embed-note"><p class="archive-note">'
                f'[Embedded content from {domain} — requires internet connection]</p>'
                f'{str(iframe)}</figure>', 'lxml'
            ).body.next
            iframe.replace_with(note)
            continue

        thumb_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        thumb_content = lib.download_image(thumb_url, session)
        if thumb_content:
            thumb_dir = legacy_dir / 'assets' / 'images' / 'youtube'
            thumb_dir.mkdir(parents=True, exist_ok=True)
            (thumb_dir / f"{video_id}.jpg").write_bytes(thumb_content)
        thumb_local = f"../../assets/images/youtube/{video_id}.jpg"

        replacement_html = lib.make_youtube_replacement(video_id, thumb_local)
        replacement = BeautifulSoup(replacement_html, 'lxml').body.next
        iframe.replace_with(replacement)
        video_records.append({'video_id': video_id, 'thumbnail_local': thumb_local})

    return video_records


def process_gists(article, session):
    """Replace GitHub Gist script tags with inline code blocks."""
    gist_records = []
    for script in article.find_all('script', src=True):
        src = script.get('src', '')
        user, gist_id = lib.extract_gist_id(src)
        if gist_id is None:
            # Non-Gist script embed — flag for review
            NEEDS_REVIEW.append({'type': 'unknown_script_embed', 'src': src})
            script.decompose()
            continue

        files = lib.fetch_gist_content(gist_id, session)
        if files is None:
            NEEDS_REVIEW.append({'type': 'gist_fetch_failed', 'gist_id': gist_id, 'src': src})
        replacement_html = lib.make_gist_replacement(user, gist_id, files)
        replacement = BeautifulSoup(replacement_html, 'lxml').body.next
        script.replace_with(replacement)
        gist_records.append({'gist_id': gist_id, 'user': user, 'files_count': len(files) if files else 0})

    return gist_records


def process_post(html_path: Path, state: dict, legacy_dir: Path, session: requests.Session) -> bool:
    """
    Process a single mirrored HTML file.
    Returns True if successfully processed, False if skipped or failed.
    """
    raw_html = html_path.read_text(encoding='utf-8', errors='replace')
    soup = BeautifulSoup(raw_html, 'lxml')

    if not lib.is_post_page(soup):
        return False

    canonical_url = lib.extract_canonical_url(soup)
    if not canonical_url:
        return False

    if canonical_url in state['completed']:
        return False

    try:
        metadata = lib.extract_metadata(soup, canonical_url)
        metadata['archived_date'] = str(_date.today())

        article = soup.find('article')
        if not article:
            return False

        # Transform embedded content (order matters: before cleaning)
        image_records = process_images(article, metadata['date'], state, legacy_dir, session)
        video_records = process_youtube(article, legacy_dir, session)
        gist_records = process_gists(article, session)

        # Clean article (strips scripts, social buttons, etc.)
        lib.clean_article(article)

        metadata['images'] = image_records
        metadata['embedded_videos'] = video_records
        metadata['embedded_gists'] = gist_records

        # Build output paths
        author_slug = metadata['author_slug'] or 'unknown'
        post_date = metadata['date'] or '0000-00-00'
        post_slug = lib.make_post_slug(canonical_url)
        filename_base = f"{post_date}-{post_slug}"

        post_dir = legacy_dir / 'posts' / author_slug
        post_dir.mkdir(parents=True, exist_ok=True)

        # Write HTML
        html_out = lib.make_html_shell(str(article), metadata)
        (post_dir / f"{filename_base}.html").write_text(html_out, encoding='utf-8')

        # Write JSON sidecar
        (post_dir / f"{filename_base}.json").write_text(
            json.dumps(metadata, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )

        state['completed'].append(canonical_url)
        return True

    except Exception as exc:
        state['failed'].append({'url': canonical_url, 'reason': str(exc), 'timestamp': str(_date.today())})
        return False


def extract_offline_css(mirror_root: Path, legacy_dir: Path, session: requests.Session) -> None:
    """
    Find the blog stylesheet URL from any mirrored HTML and fetch it.
    Save a trimmed version (typography + content rules only) to legacy/assets/article.css.
    """
    css_url = None
    for html_file in list(mirror_root.rglob('*.html'))[:20]:
        try:
            soup = BeautifulSoup(html_file.read_text(errors='replace'), 'lxml')
            link = soup.find('link', rel='stylesheet', href=re.compile(r'style.*\.css'))
            if link and link.get('href', '').startswith('http'):
                css_url = link['href']
                break
        except Exception:
            continue

    css_content = None
    if css_url:
        try:
            resp = session.get(css_url, timeout=30)
            if resp.status_code == 200:
                css_content = resp.text
        except Exception:
            pass

    assets_dir = legacy_dir / 'assets'
    assets_dir.mkdir(parents=True, exist_ok=True)

    if css_content:
        # Keep only rules that don't mention nav/sidebar/footer/menu selectors
        SKIP_PATTERNS = re.compile(
            r'(\.site-header|\.site-footer|\.widget|\.sidebar|#masthead|'
            r'\.nav-|\.navigation|\.post-navigation|\.menu|\.comment|\.wpdiscuz)', re.IGNORECASE
        )
        kept_rules = []
        for block in re.split(r'(?<=\})', css_content):
            if not SKIP_PATTERNS.search(block):
                kept_rules.append(block)
        (assets_dir / 'article.css').write_text('\n'.join(kept_rules), encoding='utf-8')
    else:
        # Fallback minimal stylesheet
        (assets_dir / 'article.css').write_text(
            "body { font-family: Georgia, serif; max-width: 780px; margin: 2rem auto; "
            "padding: 0 1rem; line-height: 1.7; color: #222; }\n"
            "h1, h2, h3 { font-family: sans-serif; }\n"
            "pre { background: #f4f4f4; padding: 1rem; overflow-x: auto; border-radius: 4px; }\n"
            "code { font-family: monospace; font-size: 0.9em; }\n"
            "img { max-width: 100%; height: auto; }\n"
            "figure { margin: 1.5rem 0; }\n"
            "figcaption { font-size: 0.85em; color: #666; text-align: center; }\n"
            ".archive-header { border-bottom: 1px solid #ccc; margin-bottom: 2rem; padding-bottom: 0.5rem; }\n"
            ".archive-note { font-size: 0.85em; color: #666; }\n"
            ".video-embed img { cursor: pointer; }\n"
            ".gist-embed pre { border-left: 4px solid #0366d6; }\n",
            encoding='utf-8'
        )


def discover_posts(mirror_root: Path) -> list[Path]:
    """
    Walk mirror_root and return paths of HTML files that match YYYY/MM/*.html pattern.
    """
    pattern = re.compile(r'/\d{4}/\d{2}/[^/]+\.html$')
    return [p for p in mirror_root.rglob('*.html') if pattern.search(str(p)) and p.is_file()]


def main():
    import logging
    logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')
    parser = argparse.ArgumentParser(description='Extract KIE blog posts from local mirror')
    parser.add_argument('--mirror', default='kie-mirror/blog.kie.org', help='Path to wget mirror root')
    parser.add_argument('--legacy', default='legacy', help='Output directory')
    parser.add_argument('--state', default='._state.json', help='State file path')
    parser.add_argument('--limit', type=int, default=0, help='Process at most N posts (0 = all)')
    args = parser.parse_args()

    mirror_root = Path(args.mirror)
    legacy_dir = Path(args.legacy)
    state_path = Path(args.state)

    if not mirror_root.exists():
        print(f"ERROR: mirror directory not found: {mirror_root}", file=sys.stderr)
        sys.exit(1)

    state = lib.load_state(state_path)
    session = requests.Session()
    session.headers['User-Agent'] = 'Mozilla/5.0 (compatible; KIE-Archive/1.0)'

    # Phase 3: offline CSS (run once)
    css_path = legacy_dir / 'assets' / 'article.css'
    if not css_path.exists():
        print("Extracting offline CSS...")
        extract_offline_css(mirror_root, legacy_dir, session)

    posts = discover_posts(mirror_root)
    print(f"Found {len(posts)} candidate post files in mirror.")

    if args.limit:
        posts = posts[:args.limit]

    processed = 0
    for i, html_path in enumerate(posts, 1):
        ok = process_post(html_path, state, legacy_dir, session)
        if ok:
            processed += 1
        if i % 50 == 0:
            lib.save_state(state, state_path)
            print(f"  Progress: {i}/{len(posts)} files examined, {processed} posts saved")
        time.sleep(0.1)  # small delay between image fetches

    lib.save_state(state, state_path)

    # Write needs-review report
    if NEEDS_REVIEW:
        review_path = legacy_dir / 'needs-review.json'
        review_path.write_text(json.dumps(NEEDS_REVIEW, indent=2), encoding='utf-8')
        print(f"\n⚠  {len(NEEDS_REVIEW)} items need review — see {review_path}")

    print(f"\nDone. {processed} posts extracted. {len(state['failed'])} failures.")
    print(f"Completed: {len(state['completed'])} total in state file.")


if __name__ == '__main__':
    main()
