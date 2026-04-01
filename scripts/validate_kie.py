#!/usr/bin/env python3
"""
KIE Blog Archive Validator
Phase 4: checks all saved posts for broken images, links, and missed transforms.

Usage:
    python scripts/validate_kie.py --legacy legacy
    python scripts/validate_kie.py --legacy legacy --skip-external
"""
import argparse
import json
import logging
import sys
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')


def check_local_images(post_path: Path, legacy_dir: Path) -> list[dict]:
    """Return list of issues for missing local images in a post file."""
    issues = []
    soup = BeautifulSoup(post_path.read_text(encoding='utf-8', errors='replace'), 'lxml')
    for img in soup.find_all('img', src=True):
        src = img['src']
        if not src.startswith('../../assets/'):
            continue
        rel = src.replace('../../', '')
        abs_path = legacy_dir / rel
        if not abs_path.exists():
            issues.append({'type': 'missing_image', 'post': str(post_path), 'src': src})
    return issues


def check_local_links(post_path: Path, legacy_dir: Path) -> list[dict]:
    """Return issues for internal links that point to missing local files."""
    issues = []
    soup = BeautifulSoup(post_path.read_text(encoding='utf-8', errors='replace'), 'lxml')
    for a in soup.find_all('a', href=True):
        href = a['href']
        if not href.startswith('../../'):
            continue
        # Strip fragment and query string before resolving to a filesystem path
        rel = href.replace('../../', '').split('#')[0].split('?')[0]
        if not rel:
            continue
        abs_path = legacy_dir / rel
        if not abs_path.exists():
            issues.append({'type': 'broken_local_link', 'post': str(post_path), 'href': href})
    return issues


def check_external_links(post_path: Path, session: requests.Session) -> list[dict]:
    """HEAD-check all external links in a post. Returns issues for non-2xx responses."""
    issues = []
    soup = BeautifulSoup(post_path.read_text(encoding='utf-8', errors='replace'), 'lxml')
    seen = set()
    for a in soup.find_all('a', href=True):
        href = a['href']
        if not href.startswith('http') or href in seen:
            continue
        seen.add(href)
        try:
            resp = session.head(href, timeout=15, allow_redirects=True)
            if resp.status_code >= 400:
                issues.append({'type': 'dead_external_link', 'post': str(post_path),
                                'href': href, 'status': resp.status_code})
        except requests.RequestException as e:
            issues.append({'type': 'dead_external_link', 'post': str(post_path),
                            'href': href, 'status': str(e)})
        time.sleep(0.2)
    return issues


def check_unreplaced_gists(post_path: Path) -> list[dict]:
    """Flag any <script src='gist.github.com'> that was not replaced."""
    issues = []
    soup = BeautifulSoup(post_path.read_text(encoding='utf-8', errors='replace'), 'lxml')
    for script in soup.find_all('script', src=True):
        if 'gist.github.com' in script.get('src', ''):
            issues.append({'type': 'unreplaced_gist', 'post': str(post_path), 'src': script['src']})
    return issues


def main():
    parser = argparse.ArgumentParser(description='Validate KIE archive posts')
    parser.add_argument('--legacy', default='legacy', help='Archive directory')
    parser.add_argument('--skip-external', action='store_true', help='Skip external link checks')
    args = parser.parse_args()

    legacy_dir = Path(args.legacy)
    session = requests.Session()
    session.headers['User-Agent'] = 'Mozilla/5.0 (compatible; KIE-Archive-Validator/1.0)'

    all_issues = []
    posts = list((legacy_dir / 'posts').rglob('*.html'))
    print(f"Validating {len(posts)} posts...")

    for i, post_path in enumerate(posts, 1):
        all_issues.extend(check_local_images(post_path, legacy_dir))
        all_issues.extend(check_local_links(post_path, legacy_dir))
        all_issues.extend(check_unreplaced_gists(post_path))
        if not args.skip_external:
            all_issues.extend(check_external_links(post_path, session))
        if i % 100 == 0:
            print(f"  {i}/{len(posts)} checked, {len(all_issues)} issues so far")

    by_type: dict[str, int] = {}
    for issue in all_issues:
        by_type.setdefault(issue['type'], 0)
        by_type[issue['type']] += 1

    report = {
        'summary': {'posts_checked': len(posts), **by_type},
        'issues': all_issues,
    }

    report_path = legacy_dir / 'validation-report.json'
    report_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(f"\nValidation complete. {len(all_issues)} issues found.")
    print(f"Report saved to {report_path}")
    for t, count in by_type.items():
        print(f"  {t}: {count}")


if __name__ == '__main__':
    main()
