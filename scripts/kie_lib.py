import hashlib
import html as html_module
import json
import logging
import re
import time
import unicodedata
from pathlib import Path
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def make_author_slug(name: str) -> str:
    """Convert an author display name to a filesystem-safe slug."""
    normalized = unicodedata.normalize('NFKD', name)
    ascii_str = normalized.encode('ascii', 'ignore').decode('ascii')
    slug = ascii_str.lower()
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-')


def make_post_slug(canonical_url: str) -> str:
    """Extract post slug from canonical URL, stripping .html extension."""
    path = urlparse(canonical_url).path.rstrip('/')
    slug = path.split('/')[-1]
    if slug.endswith('.html'):
        slug = slug[:-5]
    return slug


def load_state(path: Path) -> dict:
    """Load state file; return empty state structure if not found or corrupt."""
    if path.exists():
        try:
            with open(path) as f:
                return json.load(f)
        except json.JSONDecodeError as exc:
            logger.warning("State file %s is corrupt (%s) — starting fresh", path, exc)
    return {'completed': [], 'failed': [], 'image_cache': {}}


def save_state(state: dict, path: Path) -> None:
    """Write state file atomically via a temp file."""
    tmp = path.with_suffix('.tmp')
    with open(tmp, 'w') as f:
        json.dump(state, f, indent=2)
    tmp.rename(path)


def is_post_page(soup: BeautifulSoup) -> bool:
    """Return True if this HTML page contains a WordPress article.post element."""
    return soup.find('article', class_=lambda c: c and 'post' in c.split()) is not None


def extract_canonical_url(soup: BeautifulSoup) -> str | None:
    """Return canonical URL from <link rel='canonical'>, or None."""
    tag = soup.find('link', rel='canonical')
    if tag and tag.get('href'):
        return tag['href']
    return None


def extract_metadata(soup: BeautifulSoup, canonical_url: str) -> dict:
    """Extract all post metadata from a WordPress post page."""
    article = soup.find('article')

    # Title
    h1 = article.find('h1', class_='entry-title') if article else None
    title = h1.get_text(strip=True) if h1 else (soup.title.string if soup.title else '')

    # Author — KIE blog uses <a class="author url fn">, some themes use <a class="url fn n">
    author_tag = (
        soup.find('a', class_='author') or
        soup.find('a', class_='url fn n') or
        soup.find('span', class_='author')
    )
    author = author_tag.get_text(strip=True) if author_tag else 'Unknown'

    # Date — prefer datetime attribute on <time>, fall back to published_time meta
    time_tag = soup.find('time', class_='entry-date')
    if time_tag and time_tag.get('datetime'):
        date = time_tag['datetime'][:10]  # YYYY-MM-DD
    else:
        meta = soup.find('meta', property='article:published_time')
        date = meta['content'][:10] if meta and meta.get('content') else ''

    # Categories and tags — BS4/lxml parses rel as a list e.g. ['category', 'tag']
    categories = [a.get_text(strip=True) for a in soup.find_all('a')
                  if a.get('rel') and 'category' in a.get('rel') and 'tag' in a.get('rel')]
    tags = [a.get_text(strip=True) for a in soup.find_all('a')
            if a.get('rel') == ['tag']]

    # Excerpt — first <p> in entry-content
    content_div = article.find(class_='entry-content') if article else None
    first_p = content_div.find('p') if content_div else None
    excerpt = first_p.get_text(strip=True) if first_p else ''

    return {
        'title': title,
        'author': author,
        'author_slug': make_author_slug(author),
        'date': date,
        'categories': categories,
        'tags': tags,
        'original_url': canonical_url,
        'excerpt': excerpt,
        'archived_date': '',   # set by caller at extraction time
        'images': [],
        'embedded_videos': [],
        'embedded_gists': [],
        'other_embeds': [],
    }


def compute_image_hash(content: bytes) -> str:
    """Return first 12 hex chars of SHA-256 hash of image content."""
    return hashlib.sha256(content).hexdigest()[:12]


def get_local_image_path(original_url: str, content_hash: str, post_date: str) -> str:
    """
    Return storage path relative to legacy/assets/ for a given image.
    e.g. 'images/2023/07/abc123def456-diagram.png'
    """
    year, month = post_date[:4], post_date[5:7]
    original_filename = urlparse(original_url).path.split('/')[-1] or 'image'
    original_filename = re.sub(r'[^a-zA-Z0-9._-]', '_', original_filename)[:80]
    return f"images/{year}/{month}/{content_hash}-{original_filename}"


def download_image(url: str, session: requests.Session, retries: int = 3) -> bytes | None:
    """
    Download image bytes from url. Returns None on failure.
    Retries up to `retries` times with 2-second backoff.
    """
    for attempt in range(retries):
        try:
            resp = session.get(url, timeout=30)
            if resp.status_code == 200:
                return resp.content
            return None
        except requests.RequestException:
            if attempt < retries - 1:
                time.sleep(2)
    return None


def extract_youtube_id(url: str) -> str | None:
    """Extract YouTube video ID from embed, watch, or youtu.be URLs. Returns None if not YouTube."""
    parsed = urlparse(url)
    host = parsed.netloc.lower().replace('www.', '')
    if host == 'youtu.be':
        return parsed.path.lstrip('/')
    if host in ('youtube.com', 'youtube-nocookie.com'):
        if '/embed/' in parsed.path:
            return parsed.path.split('/embed/')[-1].split('/')[0].split('?')[0]
        qs = parse_qs(parsed.query)
        if 'v' in qs:
            return qs['v'][0]
    return None


def make_youtube_replacement(video_id: str, thumbnail_local_path: str) -> str:
    """Return HTML fragment replacing a YouTube iframe with a thumbnail + link."""
    safe_id = html_module.escape(video_id)
    safe_thumb = html_module.escape(thumbnail_local_path)
    return (
        f'<figure class="video-embed">'
        f'<a href="https://www.youtube.com/watch?v={safe_id}" target="_blank" rel="noopener">'
        f'<img src="{safe_thumb}" alt="YouTube video: {safe_id}" style="max-width:100%">'
        f'<figcaption>&#9654; Watch on YouTube</figcaption>'
        f'</a></figure>'
    )


def extract_gist_id(script_src: str) -> tuple[str | None, str | None]:
    """
    Parse gist.github.com script src.
    Returns (user, gist_id) or (None, None) if not a gist URL.
    """
    parsed = urlparse(script_src)
    if 'gist.github.com' not in parsed.netloc:
        return (None, None)
    parts = parsed.path.strip('/').split('/')
    if len(parts) >= 2:
        user = parts[0]
        gist_id = parts[1].removesuffix('.js')
        if not gist_id:
            return (None, None)
        return (user, gist_id)
    if len(parts) == 1:
        gist_id = parts[0].removesuffix('.js')
        if not gist_id:
            return (None, None)
        return (None, gist_id)
    return (None, None)


def fetch_gist_content(gist_id: str, session: requests.Session) -> list[dict] | None:
    """
    Fetch gist file content via GitHub API.
    Returns list of {'filename', 'content', 'language'} dicts, or None on failure.
    """
    try:
        resp = session.get(
            f"https://api.github.com/gists/{gist_id}",
            headers={"Accept": "application/vnd.github+json"},
            timeout=30
        )
        if resp.status_code != 200:
            return None
        data = resp.json()
        return [
            {
                'filename': fname,
                'content': fdata.get('content', ''),
                'language': fdata.get('language') or 'text',
            }
            for fname, fdata in data.get('files', {}).items()
        ]
    except requests.RequestException:
        return None


def make_gist_replacement(user: str | None, gist_id: str, files: list[dict] | None) -> str:
    """
    Return HTML fragment replacing a Gist script tag.
    If files is None (fetch failed), returns a visible archive note.
    """
    safe_user = html_module.escape(user) if user else None
    safe_gist_id = html_module.escape(gist_id)
    gist_url = (
        f"https://gist.github.com/{safe_user}/{safe_gist_id}"
        if safe_user else
        f"https://gist.github.com/{safe_gist_id}"
    )
    if not files:  # None (fetch failed) or [] (empty gist)
        return (
            f'<figure class="gist-embed">'
            f'<p class="archive-note">Gist embed could not be retrieved. '
            f'<a href="{gist_url}" target="_blank" rel="noopener">View original on GitHub Gist</a>.</p>'
            f'</figure>'
        )
    parts = []
    for f in files:
        lang = (f.get('language') or 'text').lower()
        escaped = html_module.escape(f['content'])
        parts.append(
            f'<figure class="gist-embed">'
            f'<figcaption><a href="{gist_url}" target="_blank" rel="noopener">'
            f'View on GitHub Gist: {html_module.escape(f["filename"])}</a></figcaption>'
            f'<pre><code class="language-{lang}">{escaped}</code></pre>'
            f'</figure>'
        )
    return '\n'.join(parts)


STRIP_SELECTORS = [
    'script', 'style',
    '.addtoany_share_save_container', '.addtoany_share_save',
    '.sharedaddy', '#comments', '.comments-area',
    '.author-box', '.author-description',
    '.jp-relatedposts', '.post-navigation',
    '.wpdiscuz-form-container', '[class*="wpDiscuz"]',
]

KEEP_ATTRS = {'src', 'href', 'alt', 'title', 'datetime', 'lang'}
KEEP_ATTRS_ON_CODE = {'class'}  # preserve language-X class on <code> and <pre>


def clean_article(article: BeautifulSoup) -> None:
    """
    Mutate article in-place: remove WordPress chrome, strip non-essential
    attributes while keeping content-critical ones.
    """
    # Remove unwanted elements
    for selector in STRIP_SELECTORS:
        for el in article.select(selector):
            el.decompose()

    # Strip attributes from all elements
    for tag in article.find_all(True):
        allowed = set(KEEP_ATTRS)
        if tag.name in ('code', 'pre'):
            allowed |= KEEP_ATTRS_ON_CODE
        attrs_to_remove = [k for k in list(tag.attrs.keys()) if k not in allowed]
        for attr in attrs_to_remove:
            del tag[attr]


def make_html_shell(article_html: str, metadata: dict) -> str:
    """Wrap a cleaned article HTML string in a minimal standalone HTML document."""
    title = html_module.escape(metadata.get('title', 'Untitled'))
    author = html_module.escape(metadata.get('author', ''))
    date = html_module.escape(metadata.get('date', ''))
    original_url = metadata.get('original_url', '')
    archived_date = html_module.escape(metadata.get('archived_date', ''))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — KIE Blog Archive</title>
  <meta name="author" content="{author}">
  <meta name="date" content="{date}">
  <meta name="original-url" content="{html_module.escape(original_url)}">
  <link rel="stylesheet" href="../../assets/article.css">
</head>
<body>
<header class="archive-header">
  <p class="archive-note">Archived from <a href="{html_module.escape(original_url)}">{html_module.escape(original_url)}</a> on {archived_date}.
  Original content &copy; respective authors, licensed <a href="https://creativecommons.org/licenses/by/3.0/">CC BY 3.0</a>.</p>
</header>
{article_html}
</body>
</html>"""
