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


def extract_metadata(soup: BeautifulSoup, canonical_url: str) -> dict:
    """Extract all post metadata from a WordPress post page."""
    article = soup.find('article')

    # Title
    h1 = article.find('h1', class_='entry-title') if article else None
    title = h1.get_text(strip=True) if h1 else (soup.title.string if soup.title else '')

    # Author
    author_tag = soup.find('a', class_='url fn n') or soup.find('span', class_='author')
    author = author_tag.get_text(strip=True) if author_tag else 'Unknown'

    # Date — prefer datetime attribute on <time>, fall back to published_time meta
    time_tag = soup.find('time', class_='entry-date')
    if time_tag and time_tag.get('datetime'):
        date = time_tag['datetime'][:10]  # YYYY-MM-DD
    else:
        meta = soup.find('meta', property='article:published_time')
        date = meta['content'][:10] if meta and meta.get('content') else ''

    # Categories and tags
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
