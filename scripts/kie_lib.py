import hashlib
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import urlparse


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
    """Load state file; return empty state structure if not found."""
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {'completed': [], 'failed': [], 'image_cache': {}}


def save_state(state: dict, path: Path) -> None:
    """Write state file atomically via a temp file."""
    tmp = path.with_suffix('.tmp')
    with open(tmp, 'w') as f:
        json.dump(state, f, indent=2)
    tmp.rename(path)


from bs4 import BeautifulSoup, Tag


def is_post_page(soup: BeautifulSoup) -> bool:
    """Return True if this HTML page contains a WordPress article.post element."""
    return soup.find('article', class_=lambda c: c and 'post' in c.split()) is not None


def extract_canonical_url(soup: BeautifulSoup) -> str | None:
    """Return canonical URL from <link rel='canonical'>, or None."""
    tag = soup.find('link', rel='canonical')
    if tag and tag.get('href'):
        return tag['href']
    return None
