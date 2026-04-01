#!/usr/bin/env python3
"""
KIE Blog Archive Index Generator
Phase 5: generates legacy/index.html

Usage:
    python scripts/generate_index.py --legacy legacy
"""
import argparse
import html as html_module
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


def load_all_sidecars(legacy_dir: Path) -> list[dict]:
    """Load all JSON sidecar files from legacy/posts/."""
    sidecars = []
    for json_path in (legacy_dir / 'posts').rglob('*.json'):
        try:
            sidecars.append(json.loads(json_path.read_text(encoding='utf-8')))
        except Exception:
            continue
    return sidecars


def group_by_author(posts: list[dict]) -> dict[str, list[dict]]:
    """Group posts by author_slug, each group sorted by date descending."""
    grouped: dict[str, list[dict]] = {}
    for post in posts:
        slug = post.get('author_slug', 'unknown')
        grouped.setdefault(slug, []).append(post)
    for slug in grouped:
        grouped[slug].sort(key=lambda p: p.get('date', ''), reverse=True)
    return dict(sorted(grouped.items()))


def render_index(grouped: dict[str, list[dict]], total: int, archived_date: str) -> str:
    """Return a complete standalone HTML index page."""
    author_sections = []
    for author_slug, posts in grouped.items():
        author_name = html_module.escape(posts[0].get('author', author_slug))
        rows = []
        for post in posts:
            post_date = post.get('date', '0000-00-00')
            title = html_module.escape(post.get('title', 'Untitled'))
            url_path = urlparse(post.get('original_url', '')).path.rstrip('/')
            post_slug = url_path.split('/')[-1].replace('.html', '')
            local_href = html_module.escape(f"posts/{author_slug}/{post_date}-{post_slug}.html")
            cats = ' '.join(
                f'<span class="badge">{html_module.escape(c)}</span>'
                for c in post.get('categories', [])
            )
            rows.append(
                f'<tr><td class="date">{html_module.escape(post_date)}</td>'
                f'<td><a href="{local_href}">{title}</a> {cats}</td></tr>'
            )
        author_sections.append(
            f'\n<section>\n'
            f'  <h2 id="{html_module.escape(author_slug)}">'
            f'{author_name} <small>({len(posts)} posts)</small></h2>\n'
            f'  <table><tbody>\n'
            f'  {"".join(rows)}\n'
            f'  </tbody></table>\n'
            f'</section>'
        )

    toc_links = ''.join(
        f'<a href="#{html_module.escape(slug)}">'
        f'{html_module.escape(posts[0].get("author", slug))} ({len(posts)})</a>'
        for slug, posts in grouped.items()
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>KIE Blog Archive — {total} posts</title>
  <style>
    body {{ font-family: sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; color: #222; }}
    h1 {{ border-bottom: 2px solid #cc0000; padding-bottom: 0.5rem; }}
    h2 {{ margin-top: 2rem; color: #333; }}
    small {{ font-weight: normal; color: #666; font-size: 0.75em; }}
    table {{ width: 100%; border-collapse: collapse; margin-bottom: 1rem; }}
    td {{ padding: 0.3rem 0.5rem; border-bottom: 1px solid #eee; vertical-align: top; }}
    td.date {{ white-space: nowrap; color: #666; width: 7rem; }}
    .badge {{ background: #eef; color: #336; font-size: 0.75em; padding: 1px 6px; border-radius: 3px; margin-left: 4px; }}
    a {{ color: #0366d6; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    #toc {{ column-count: 3; column-gap: 1rem; margin: 1rem 0 2rem; }}
    #toc a {{ display: block; padding: 2px 0; }}
  </style>
</head>
<body>
<h1>KIE Blog Archive</h1>
<p>{total} posts archived on {html_module.escape(archived_date)}.</p>
<nav id="toc">
{toc_links}
</nav>
{"".join(author_sections)}
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description='Generate KIE archive index page')
    parser.add_argument('--legacy', default='legacy')
    args = parser.parse_args()

    legacy_dir = Path(args.legacy)
    sidecars = load_all_sidecars(legacy_dir)
    print(f"Loaded {len(sidecars)} post sidecars.")
    grouped = group_by_author(sidecars)
    html = render_index(grouped, total=len(sidecars), archived_date=str(date.today()))
    out = legacy_dir / 'index.html'
    out.write_text(html, encoding='utf-8')
    print(f"Index written to {out}")


if __name__ == '__main__':
    main()
