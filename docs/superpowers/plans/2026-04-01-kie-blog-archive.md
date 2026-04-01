# KIE Blog Archive Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a local, offline-capable HTML archive of all ~1,800 posts from blog.kie.org, stored in `legacy/`, with images cached, YouTube replaced by thumbnails, and Gists inlined.

**Architecture:** Two phases — a `wget` HTML-only mirror into gitignored `kie-mirror/`, then a Python extractor that reads the mirror, transforms content, downloads article images, and writes clean standalone HTML + JSON sidecar per post. A separate validator and index generator run after extraction.

**Tech Stack:** Python 3.10+, `requests`, `beautifulsoup4`, `lxml`, `pytest`, `wget` (system CLI)

---

## File Structure

| File | Responsibility |
|---|---|
| `scripts/requirements.txt` | Python dependencies |
| `scripts/kie_lib.py` | All pure, testable functions (slug, state, parsing, transforms) |
| `scripts/extract_kie.py` | Orchestration: discovers posts, calls lib functions, writes output |
| `scripts/validate_kie.py` | Post-extraction validation pass |
| `scripts/generate_index.py` | Generates `legacy/index.html` |
| `tests/test_kie_lib.py` | Tests for all kie_lib functions |
| `tests/test_validate.py` | Tests for validator logic |
| `tests/test_generate_index.py` | Tests for index generator |
| `.gitignore` | Add `kie-mirror/` and `._state.json` |
| `legacy/assets/article.css` | Written by extract_kie.py Phase 3 |

---

## Task 1: Project Setup

**Files:**
- Create: `scripts/requirements.txt`
- Create: `tests/__init__.py`
- Modify: `.gitignore`

- [ ] **Step 1: Create requirements.txt**

```
# scripts/requirements.txt
requests==2.31.0
beautifulsoup4==4.12.2
lxml==4.9.3
pytest==7.4.0
```

- [ ] **Step 2: Install dependencies**

```bash
pip install -r scripts/requirements.txt
```

Expected: all packages install without error.

- [ ] **Step 3: Create tests package**

```bash
mkdir -p tests
touch tests/__init__.py
```

- [ ] **Step 4: Update .gitignore**

Open `.gitignore` and append:

```
kie-mirror/
._state.json
legacy/
```

Note: `legacy/` is gitignored for now — it will be committed separately once the archive is complete and reviewed.

- [ ] **Step 5: Commit**

```bash
git add scripts/requirements.txt tests/__init__.py .gitignore
git commit -m "chore: scaffold KIE archive scripts and gitignore"
```

---

## Task 2: Author Slug and Post Slug Utilities

**Files:**
- Create: `scripts/kie_lib.py`
- Create: `tests/test_kie_lib.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_kie_lib.py`:

```python
import pytest
import sys
sys.path.insert(0, 'scripts')
from kie_lib import make_author_slug, make_post_slug


def test_make_author_slug_simple():
    assert make_author_slug("Mark Proctor") == "mark-proctor"


def test_make_author_slug_accents():
    assert make_author_slug("Gonzalo Muñoz Fernández") == "gonzalo-munoz-fernandez"


def test_make_author_slug_multiple_spaces():
    assert make_author_slug("John  Doe") == "john-doe"


def test_make_author_slug_already_ascii():
    assert make_author_slug("Jozef Marko") == "jozef-marko"


def test_make_author_slug_single_name():
    assert make_author_slug("Trilobite") == "trilobite"


def test_make_post_slug_standard():
    assert make_post_slug("https://blog.kie.org/2023/07/groupby-a-new-way.html") == "groupby-a-new-way"


def test_make_post_slug_no_html_extension():
    assert make_post_slug("https://blog.kie.org/2023/07/some-post") == "some-post"


def test_make_post_slug_trailing_slash():
    assert make_post_slug("https://blog.kie.org/2023/07/some-post/") == "some-post"
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
cd /Users/mdproctor/mdproctor.github.io
python -m pytest tests/test_kie_lib.py::test_make_author_slug_simple -v
```

Expected: `ModuleNotFoundError: No module named 'kie_lib'`

- [ ] **Step 3: Implement in kie_lib.py**

Create `scripts/kie_lib.py`:

```python
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
```

- [ ] **Step 4: Run all slug tests**

```bash
python -m pytest tests/test_kie_lib.py -k "slug" -v
```

Expected: 8 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/kie_lib.py tests/test_kie_lib.py
git commit -m "feat: author slug and post slug normalisation"
```

---

## Task 3: State File Management

**Files:**
- Modify: `scripts/kie_lib.py`
- Modify: `tests/test_kie_lib.py`

- [ ] **Step 1: Write failing tests**

Append to `tests/test_kie_lib.py`:

```python
import json
import tempfile
from pathlib import Path
from kie_lib import load_state, save_state


def test_load_state_missing_file():
    with tempfile.TemporaryDirectory() as d:
        state = load_state(Path(d) / '._state.json')
    assert state == {'completed': [], 'failed': [], 'image_cache': {}}


def test_load_state_existing_file():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / '._state.json'
        p.write_text(json.dumps({'completed': ['http://a.com'], 'failed': [], 'image_cache': {}}))
        state = load_state(p)
    assert state['completed'] == ['http://a.com']


def test_save_state_roundtrip():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / '._state.json'
        original = {'completed': ['http://x.com'], 'failed': [], 'image_cache': {'abc': 'path'}}
        save_state(original, p)
        loaded = load_state(p)
    assert loaded == original


def test_save_state_atomic(tmp_path):
    p = tmp_path / '._state.json'
    save_state({'completed': [], 'failed': [], 'image_cache': {}}, p)
    assert p.exists()
    assert not (tmp_path / '._state.tmp').exists()
```

- [ ] **Step 2: Run to confirm failure**

```bash
python -m pytest tests/test_kie_lib.py -k "state" -v
```

Expected: `ImportError: cannot import name 'load_state'`

- [ ] **Step 3: Implement in kie_lib.py**

Append to `scripts/kie_lib.py`:

```python
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
```

- [ ] **Step 4: Run state tests**

```bash
python -m pytest tests/test_kie_lib.py -k "state" -v
```

Expected: 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/kie_lib.py tests/test_kie_lib.py
git commit -m "feat: resumable state file load/save"
```

---

## Task 4: Post Discovery

**Files:**
- Modify: `scripts/kie_lib.py`
- Modify: `tests/test_kie_lib.py`

- [ ] **Step 1: Write failing tests**

Append to `tests/test_kie_lib.py`:

```python
from kie_lib import is_post_page, extract_canonical_url
from bs4 import BeautifulSoup

POST_HTML = """
<html><head>
  <link rel="canonical" href="https://blog.kie.org/2023/07/groupby.html">
</head><body>
  <article class="post type-post">
    <h1 class="entry-title">Test Post</h1>
  </article>
</body></html>
"""

INDEX_HTML = """
<html><head></head><body>
  <div class="post-listing">not an article</div>
</body></html>
"""


def test_is_post_page_true():
    soup = BeautifulSoup(POST_HTML, 'lxml')
    assert is_post_page(soup) is True


def test_is_post_page_false_for_index():
    soup = BeautifulSoup(INDEX_HTML, 'lxml')
    assert is_post_page(soup) is False


def test_extract_canonical_url():
    soup = BeautifulSoup(POST_HTML, 'lxml')
    assert extract_canonical_url(soup) == "https://blog.kie.org/2023/07/groupby.html"


def test_extract_canonical_url_missing():
    soup = BeautifulSoup(INDEX_HTML, 'lxml')
    assert extract_canonical_url(soup) is None
```

- [ ] **Step 2: Run to confirm failure**

```bash
python -m pytest tests/test_kie_lib.py -k "post_page or canonical" -v
```

Expected: `ImportError: cannot import name 'is_post_page'`

- [ ] **Step 3: Implement**

Append to `scripts/kie_lib.py`:

```python
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
```

- [ ] **Step 4: Run tests**

```bash
python -m pytest tests/test_kie_lib.py -k "post_page or canonical" -v
```

Expected: 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/kie_lib.py tests/test_kie_lib.py
git commit -m "feat: post discovery helpers"
```

---

## Task 5: Metadata Extraction

**Files:**
- Modify: `scripts/kie_lib.py`
- Modify: `tests/test_kie_lib.py`

- [ ] **Step 1: Write failing tests**

Append to `tests/test_kie_lib.py`:

```python
from kie_lib import extract_metadata

METADATA_HTML = """
<html><head>
  <link rel="canonical" href="https://blog.kie.org/2023/07/groupby.html">
</head><body>
<article class="post type-post">
  <header class="entry-header">
    <h1 class="entry-title">Groupby – a new way</h1>
    <div class="entry-meta">
      <span class="author vcard">
        <a class="url fn n" href="#">Christopher Chianelli</a>
      </span>
      <time class="entry-date published" datetime="2023-07-11T10:00:00+00:00">July 11, 2023</time>
    </div>
    <span class="cat-links"><a rel="category tag" href="#">Rules</a></span>
    <span class="tag-links"><a rel="tag" href="#">DRL</a><a rel="tag" href="#">Drools</a></span>
  </header>
  <div class="entry-content"><p>First paragraph here.</p></div>
</article>
</body></html>
"""


def test_extract_metadata_title():
    soup = BeautifulSoup(METADATA_HTML, 'lxml')
    meta = extract_metadata(soup, "https://blog.kie.org/2023/07/groupby.html")
    assert meta['title'] == "Groupby – a new way"


def test_extract_metadata_author():
    soup = BeautifulSoup(METADATA_HTML, 'lxml')
    meta = extract_metadata(soup, "https://blog.kie.org/2023/07/groupby.html")
    assert meta['author'] == "Christopher Chianelli"
    assert meta['author_slug'] == "christopher-chianelli"


def test_extract_metadata_date():
    soup = BeautifulSoup(METADATA_HTML, 'lxml')
    meta = extract_metadata(soup, "https://blog.kie.org/2023/07/groupby.html")
    assert meta['date'] == "2023-07-11"


def test_extract_metadata_categories():
    soup = BeautifulSoup(METADATA_HTML, 'lxml')
    meta = extract_metadata(soup, "https://blog.kie.org/2023/07/groupby.html")
    assert meta['categories'] == ["Rules"]


def test_extract_metadata_tags():
    soup = BeautifulSoup(METADATA_HTML, 'lxml')
    meta = extract_metadata(soup, "https://blog.kie.org/2023/07/groupby.html")
    assert set(meta['tags']) == {"DRL", "Drools"}


def test_extract_metadata_excerpt():
    soup = BeautifulSoup(METADATA_HTML, 'lxml')
    meta = extract_metadata(soup, "https://blog.kie.org/2023/07/groupby.html")
    assert meta['excerpt'] == "First paragraph here."


def test_extract_metadata_original_url():
    soup = BeautifulSoup(METADATA_HTML, 'lxml')
    meta = extract_metadata(soup, "https://blog.kie.org/2023/07/groupby.html")
    assert meta['original_url'] == "https://blog.kie.org/2023/07/groupby.html"
```

- [ ] **Step 2: Run to confirm failure**

```bash
python -m pytest tests/test_kie_lib.py -k "metadata" -v
```

Expected: `ImportError: cannot import name 'extract_metadata'`

- [ ] **Step 3: Implement**

Append to `scripts/kie_lib.py`:

```python
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
    categories = [a.get_text(strip=True) for a in soup.find_all('a', rel=lambda r: r and 'category tag' in ' '.join(r))]
    tags = [a.get_text(strip=True) for a in soup.find_all('a', rel=lambda r: r and r == ['tag'])]

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
```

- [ ] **Step 4: Run tests**

```bash
python -m pytest tests/test_kie_lib.py -k "metadata" -v
```

Expected: 7 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/kie_lib.py tests/test_kie_lib.py
git commit -m "feat: metadata extraction from WordPress HTML"
```

---

## Task 6: Image Download and Deduplication

**Files:**
- Modify: `scripts/kie_lib.py`
- Modify: `tests/test_kie_lib.py`

- [ ] **Step 1: Write failing tests**

Append to `tests/test_kie_lib.py`:

```python
from unittest.mock import patch, MagicMock
from kie_lib import compute_image_hash, get_local_image_path, download_image


def test_compute_image_hash_consistent():
    content = b'fake image bytes'
    h1 = compute_image_hash(content)
    h2 = compute_image_hash(content)
    assert h1 == h2
    assert len(h1) == 12


def test_compute_image_hash_different_content():
    assert compute_image_hash(b'aaa') != compute_image_hash(b'bbb')


def test_get_local_image_path_structure():
    path = get_local_image_path(
        "https://blog.kie.org/wp-content/uploads/2023/07/diagram.png",
        "abc123def456",
        "2023-07-11"
    )
    assert path == "images/2023/07/abc123def456-diagram.png"


def test_get_local_image_path_external_url():
    path = get_local_image_path(
        "https://lh4.googleusercontent.com/some-long-id",
        "deadbeef1234",
        "2022-01-15"
    )
    assert path == "images/2022/01/deadbeef1234-some-long-id"


def test_download_image_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'fake bytes'
    mock_session = MagicMock()
    mock_session.get.return_value = mock_response

    result = download_image("https://example.com/img.png", mock_session)
    assert result == b'fake bytes'


def test_download_image_failure_returns_none():
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_session = MagicMock()
    mock_session.get.return_value = mock_response

    result = download_image("https://example.com/missing.png", mock_session)
    assert result is None
```

- [ ] **Step 2: Run to confirm failure**

```bash
python -m pytest tests/test_kie_lib.py -k "image" -v
```

Expected: `ImportError: cannot import name 'compute_image_hash'`

- [ ] **Step 3: Implement**

Append to `scripts/kie_lib.py`:

```python
import time
import requests


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
```

- [ ] **Step 4: Run image tests**

```bash
python -m pytest tests/test_kie_lib.py -k "image" -v
```

Expected: 6 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/kie_lib.py tests/test_kie_lib.py
git commit -m "feat: image download with SHA-256 deduplication"
```

---

## Task 7: YouTube Iframe Replacement

**Files:**
- Modify: `scripts/kie_lib.py`
- Modify: `tests/test_kie_lib.py`

- [ ] **Step 1: Write failing tests**

Append to `tests/test_kie_lib.py`:

```python
from kie_lib import extract_youtube_id, make_youtube_replacement


def test_extract_youtube_id_embed_url():
    assert extract_youtube_id("https://www.youtube.com/embed/dQw4w9WgXcQ") == "dQw4w9WgXcQ"


def test_extract_youtube_id_watch_url():
    assert extract_youtube_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"


def test_extract_youtube_id_youtu_be():
    assert extract_youtube_id("https://youtu.be/dQw4w9WgXcQ") == "dQw4w9WgXcQ"


def test_extract_youtube_id_not_youtube():
    assert extract_youtube_id("https://vimeo.com/12345") is None


def test_make_youtube_replacement_contains_thumbnail():
    html = make_youtube_replacement("dQw4w9WgXcQ", "../../assets/images/youtube/dQw4w9WgXcQ.jpg")
    assert "dQw4w9WgXcQ.jpg" in html
    assert "youtube.com/watch?v=dQw4w9WgXcQ" in html
    assert "<figure" in html
    assert "Watch on YouTube" in html
```

- [ ] **Step 2: Run to confirm failure**

```bash
python -m pytest tests/test_kie_lib.py -k "youtube" -v
```

Expected: `ImportError: cannot import name 'extract_youtube_id'`

- [ ] **Step 3: Implement**

Append to `scripts/kie_lib.py`:

```python
from urllib.parse import urlparse, urljoin, parse_qs


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
    return (
        f'<figure class="video-embed">'
        f'<a href="https://www.youtube.com/watch?v={video_id}" target="_blank" rel="noopener">'
        f'<img src="{thumbnail_local_path}" alt="YouTube video: {video_id}" style="max-width:100%">'
        f'<figcaption>&#9654; Watch on YouTube</figcaption>'
        f'</a></figure>'
    )
```

- [ ] **Step 4: Run tests**

```bash
python -m pytest tests/test_kie_lib.py -k "youtube" -v
```

Expected: 5 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/kie_lib.py tests/test_kie_lib.py
git commit -m "feat: YouTube iframe extraction and thumbnail replacement"
```

---

## Task 8: GitHub Gist Inlining

**Files:**
- Modify: `scripts/kie_lib.py`
- Modify: `tests/test_kie_lib.py`

- [ ] **Step 1: Write failing tests**

Append to `tests/test_kie_lib.py`:

```python
from kie_lib import extract_gist_id, fetch_gist_content, make_gist_replacement


def test_extract_gist_id_standard():
    assert extract_gist_id("https://gist.github.com/user/abc123def.js") == ("user", "abc123def")


def test_extract_gist_id_no_user():
    assert extract_gist_id("https://gist.github.com/abc123def.js") == (None, "abc123def")


def test_extract_gist_id_not_gist():
    assert extract_gist_id("https://example.com/script.js") == (None, None)


def test_fetch_gist_content_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'files': {
            'example.java': {'content': 'public class Foo {}', 'language': 'Java'},
        }
    }
    mock_session = MagicMock()
    mock_session.get.return_value = mock_response

    files = fetch_gist_content("abc123", mock_session)
    assert files == [{'filename': 'example.java', 'content': 'public class Foo {}', 'language': 'Java'}]


def test_fetch_gist_content_failure_returns_none():
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_session = MagicMock()
    mock_session.get.return_value = mock_response

    result = fetch_gist_content("missing", mock_session)
    assert result is None


def test_make_gist_replacement_single_file():
    files = [{'filename': 'Rule.drl', 'content': 'rule "X" end', 'language': 'Drools'}]
    html = make_gist_replacement("user", "abc123", files)
    assert 'gist.github.com/user/abc123' in html
    assert 'Rule.drl' in html
    assert 'rule &quot;X&quot; end' in html or 'rule "X" end' in html
    assert '<pre>' in html
    assert 'language-Drools' in html or 'language-drools' in html


def test_make_gist_replacement_missing_gist():
    html = make_gist_replacement("user", "abc123", None)
    assert 'gist.github.com/user/abc123' in html
    assert 'archive-note' in html
```

- [ ] **Step 2: Run to confirm failure**

```bash
python -m pytest tests/test_kie_lib.py -k "gist" -v
```

Expected: `ImportError: cannot import name 'extract_gist_id'`

- [ ] **Step 3: Implement**

Append to `scripts/kie_lib.py`:

```python
import html as html_module


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
        gist_id = parts[1].replace('.js', '')
        return (user, gist_id)
    if len(parts) == 1:
        return (None, parts[0].replace('.js', ''))
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
    gist_url = f"https://gist.github.com/{user}/{gist_id}" if user else f"https://gist.github.com/{gist_id}"
    if files is None:
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
```

- [ ] **Step 4: Run tests**

```bash
python -m pytest tests/test_kie_lib.py -k "gist" -v
```

Expected: 7 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/kie_lib.py tests/test_kie_lib.py
git commit -m "feat: GitHub Gist detection, API fetch, and inline code replacement"
```

---

## Task 9: Content Cleaning

**Files:**
- Modify: `scripts/kie_lib.py`
- Modify: `tests/test_kie_lib.py`

- [ ] **Step 1: Write failing tests**

Append to `tests/test_kie_lib.py`:

```python
from kie_lib import clean_article

DIRTY_HTML = """
<article class="post">
  <div class="entry-content">
    <p>Good content.</p>
    <script>alert('bad')</script>
    <style>.foo { color: red }</style>
    <div class="addtoany_share_save_container">Share</div>
    <div id="comments">Comments</div>
    <div class="author-box">Author bio</div>
    <div class="jp-relatedposts">Related posts</div>
    <img src="image.png" class="wp-image-123" id="img1" alt="a photo">
    <pre class="wp-block-code"><code class="language-java">int x = 1;</code></pre>
  </div>
</article>
"""


def test_clean_article_removes_scripts():
    soup = BeautifulSoup(DIRTY_HTML, 'lxml')
    article = soup.find('article')
    clean_article(article)
    assert article.find('script') is None


def test_clean_article_removes_styles():
    soup = BeautifulSoup(DIRTY_HTML, 'lxml')
    article = soup.find('article')
    clean_article(article)
    assert article.find('style') is None


def test_clean_article_removes_share_buttons():
    soup = BeautifulSoup(DIRTY_HTML, 'lxml')
    article = soup.find('article')
    clean_article(article)
    assert article.find(class_='addtoany_share_save_container') is None


def test_clean_article_removes_comments_section():
    soup = BeautifulSoup(DIRTY_HTML, 'lxml')
    article = soup.find('article')
    clean_article(article)
    assert article.find(id='comments') is None


def test_clean_article_removes_author_box():
    soup = BeautifulSoup(DIRTY_HTML, 'lxml')
    article = soup.find('article')
    clean_article(article)
    assert article.find(class_='author-box') is None


def test_clean_article_preserves_good_content():
    soup = BeautifulSoup(DIRTY_HTML, 'lxml')
    article = soup.find('article')
    clean_article(article)
    assert article.find('p') is not None
    assert 'Good content.' in article.get_text()


def test_clean_article_strips_wp_classes_from_img():
    soup = BeautifulSoup(DIRTY_HTML, 'lxml')
    article = soup.find('article')
    clean_article(article)
    img = article.find('img')
    assert img is not None
    assert img.get('class') is None
    assert img.get('id') is None
    assert img.get('alt') == 'a photo'


def test_clean_article_preserves_code_language_class():
    soup = BeautifulSoup(DIRTY_HTML, 'lxml')
    article = soup.find('article')
    clean_article(article)
    code = article.find('code')
    assert code is not None
    assert 'language-java' in code.get('class', [])
```

- [ ] **Step 2: Run to confirm failure**

```bash
python -m pytest tests/test_kie_lib.py -k "clean" -v
```

Expected: `ImportError: cannot import name 'clean_article'`

- [ ] **Step 3: Implement**

Append to `scripts/kie_lib.py`:

```python
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


def clean_article(article: Tag) -> None:
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
```

- [ ] **Step 4: Run tests**

```bash
python -m pytest tests/test_kie_lib.py -k "clean" -v
```

Expected: 8 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/kie_lib.py tests/test_kie_lib.py
git commit -m "feat: article content cleaning, attribute stripping"
```

---

## Task 10: HTML Shell Generation

**Files:**
- Modify: `scripts/kie_lib.py`
- Modify: `tests/test_kie_lib.py`

- [ ] **Step 1: Write failing tests**

Append to `tests/test_kie_lib.py`:

```python
from kie_lib import make_html_shell

SAMPLE_META = {
    'title': 'Test Post',
    'author': 'Mark Proctor',
    'date': '2022-07-29',
    'original_url': 'https://blog.kie.org/2022/07/ibm-rht.html',
    'archived_date': '2026-04-01',
}


def test_make_html_shell_valid_html():
    soup = BeautifulSoup(DIRTY_HTML, 'lxml')
    article = soup.find('article')
    result = make_html_shell(str(article), SAMPLE_META)
    assert result.startswith('<!DOCTYPE html>')
    assert '<html' in result
    assert '</html>' in result


def test_make_html_shell_includes_title():
    soup = BeautifulSoup(DIRTY_HTML, 'lxml')
    article = soup.find('article')
    result = make_html_shell(str(article), SAMPLE_META)
    assert 'Test Post' in result


def test_make_html_shell_links_css():
    soup = BeautifulSoup(DIRTY_HTML, 'lxml')
    article = soup.find('article')
    result = make_html_shell(str(article), SAMPLE_META)
    assert '../../assets/article.css' in result


def test_make_html_shell_includes_archive_note():
    soup = BeautifulSoup(DIRTY_HTML, 'lxml')
    article = soup.find('article')
    result = make_html_shell(str(article), SAMPLE_META)
    assert 'blog.kie.org/2022/07/ibm-rht.html' in result
    assert 'Archived from' in result


def test_make_html_shell_includes_meta_tags():
    soup = BeautifulSoup(DIRTY_HTML, 'lxml')
    article = soup.find('article')
    result = make_html_shell(str(article), SAMPLE_META)
    assert 'name="author"' in result
    assert 'Mark Proctor' in result
    assert 'name="date"' in result
    assert '2022-07-29' in result
```

- [ ] **Step 2: Run to confirm failure**

```bash
python -m pytest tests/test_kie_lib.py -k "html_shell" -v
```

Expected: `ImportError: cannot import name 'make_html_shell'`

- [ ] **Step 3: Implement**

Append to `scripts/kie_lib.py`:

```python
def make_html_shell(article_html: str, metadata: dict) -> str:
    """Wrap a cleaned article HTML string in a minimal standalone HTML document."""
    title = html_module.escape(metadata.get('title', 'Untitled'))
    author = html_module.escape(metadata.get('author', ''))
    date = metadata.get('date', '')
    original_url = metadata.get('original_url', '')
    archived_date = metadata.get('archived_date', '')

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
```

- [ ] **Step 4: Run tests**

```bash
python -m pytest tests/test_kie_lib.py -k "html_shell" -v
```

Expected: 5 tests PASS.

- [ ] **Step 5: Run full test suite**

```bash
python -m pytest tests/test_kie_lib.py -v
```

Expected: all tests PASS.

- [ ] **Step 6: Commit**

```bash
git add scripts/kie_lib.py tests/test_kie_lib.py
git commit -m "feat: standalone HTML shell wrapper with archive metadata"
```

---

## Task 11: Main Extractor Orchestration

**Files:**
- Create: `scripts/extract_kie.py`

This script is orchestration — it wires together all `kie_lib` functions. Integration tests would require a real mirror; focus on structure and manual spot-checking after a test run on 5 posts.

- [ ] **Step 1: Create extract_kie.py**

```python
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
import os
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


def process_youtube(article, state, legacy_dir, session):
    """Replace YouTube iframes with thumbnail images + links."""
    video_records = []
    for iframe in article.find_all('iframe'):
        src = iframe.get('src', '')
        video_id = lib.extract_youtube_id(src)
        if video_id is None:
            # Non-YouTube iframe — flag for review
            domain = src.split('/')[2] if src.startswith('http') else 'unknown'
            NEEDS_REVIEW.append({'type': 'unknown_iframe', 'src': src, 'domain': domain})
            iframe.replace_with(BeautifulSoup(
                f'<figure class="embed-note"><p class="archive-note">'
                f'[Embedded content from {domain} — requires internet connection]</p>'
                f'{str(iframe)}</figure>', 'lxml'
            ).body.next)
            continue

        thumb_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        thumb_content = lib.download_image(thumb_url, session)
        if thumb_content:
            thumb_dir = legacy_dir / 'assets' / 'images' / 'youtube'
            thumb_dir.mkdir(parents=True, exist_ok=True)
            (thumb_dir / f"{video_id}.jpg").write_bytes(thumb_content)
        thumb_local = f"../../assets/images/youtube/{video_id}.jpg"

        replacement_html = lib.make_youtube_replacement(video_id, thumb_local)
        iframe.replace_with(BeautifulSoup(replacement_html, 'lxml').body.next)
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
        script.replace_with(BeautifulSoup(replacement_html, 'lxml').body.next)
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
        video_records = process_youtube(article, state, legacy_dir, session)
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
            r'\.nav-|\.navigation|\.menu|\.comment|\.wpdiscuz)', re.IGNORECASE
        )
        kept_rules = []
        # Simple block-level extraction
        for block in re.split(r'(?<=\})', css_content):
            if not SKIP_PATTERNS.search(block):
                kept_rules.append(block)
        (assets_dir / 'article.css').write_text('\n'.join(kept_rules), encoding='utf-8')
    else:
        # Fallback minimal stylesheet
        (assets_dir / 'article.css').write_text("""
body { font-family: Georgia, serif; max-width: 780px; margin: 2rem auto; padding: 0 1rem; line-height: 1.7; color: #222; }
h1, h2, h3 { font-family: sans-serif; }
pre { background: #f4f4f4; padding: 1rem; overflow-x: auto; border-radius: 4px; }
code { font-family: monospace; font-size: 0.9em; }
img { max-width: 100%; height: auto; }
figure { margin: 1.5rem 0; }
figcaption { font-size: 0.85em; color: #666; text-align: center; }
.archive-header { border-bottom: 1px solid #ccc; margin-bottom: 2rem; padding-bottom: 0.5rem; }
.archive-note { font-size: 0.85em; color: #666; }
.video-embed img { cursor: pointer; }
.gist-embed pre { border-left: 4px solid #0366d6; }
""", encoding='utf-8')


def discover_posts(mirror_root: Path) -> list[Path]:
    """
    Walk mirror_root and return paths of HTML files that match YYYY/MM/*.html pattern.
    """
    pattern = re.compile(r'/\d{4}/\d{2}/[^/]+\.html$')
    return [p for p in mirror_root.rglob('*.html') if pattern.search(str(p))]


def main():
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
```

- [ ] **Step 2: Smoke test on 5 posts (requires mirror to exist — skip if mirror not yet downloaded)**

```bash
python scripts/extract_kie.py --mirror kie-mirror/blog.kie.org --legacy legacy --limit 5
```

Expected output similar to:
```
Extracting offline CSS...
Found 2100 candidate post files in mirror.
Done. 5 posts extracted. 0 failures.
```

Check `legacy/posts/` contains one author folder with 5 `.html` and 5 `.json` files.

- [ ] **Step 3: Commit**

```bash
git add scripts/extract_kie.py
git commit -m "feat: main extraction orchestrator (images, YouTube, Gists, HTML shell)"
```

---

## Task 12: Validation Pass

**Files:**
- Create: `scripts/validate_kie.py`
- Create: `tests/test_validate.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_validate.py`:

```python
import sys, tempfile, json
from pathlib import Path
sys.path.insert(0, 'scripts')
from validate_kie import check_local_images, check_unreplaced_gists
from bs4 import BeautifulSoup


def _write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def test_check_local_images_all_present(tmp_path):
    img_path = tmp_path / 'assets' / 'images' / '2023' / '07' / 'abc-img.png'
    img_path.parent.mkdir(parents=True, exist_ok=True)
    img_path.write_bytes(b'fake')

    html = f'<html><body><img src="../../assets/images/2023/07/abc-img.png"></body></html>'
    post_path = tmp_path / 'posts' / 'author' / '2023-07-01-post.html'
    _write(post_path, html)

    issues = check_local_images(post_path, tmp_path)
    assert issues == []


def test_check_local_images_missing(tmp_path):
    html = '<html><body><img src="../../assets/images/2023/07/missing.png"></body></html>'
    post_path = tmp_path / 'posts' / 'author' / '2023-07-01-post.html'
    _write(post_path, html)

    issues = check_local_images(post_path, tmp_path)
    assert len(issues) == 1
    assert issues[0]['type'] == 'missing_image'


def test_check_unreplaced_gists_clean(tmp_path):
    html = '<html><body><pre><code>code here</code></pre></body></html>'
    post_path = tmp_path / 'posts' / 'author' / '2023-07-01-post.html'
    _write(post_path, html)
    assert check_unreplaced_gists(post_path) == []


def test_check_unreplaced_gists_found(tmp_path):
    html = '<html><body><script src="https://gist.github.com/user/abc.js"></script></body></html>'
    post_path = tmp_path / 'posts' / 'author' / '2023-07-01-post.html'
    _write(post_path, html)
    issues = check_unreplaced_gists(post_path)
    assert len(issues) == 1
    assert issues[0]['type'] == 'unreplaced_gist'
```

- [ ] **Step 2: Run to confirm failure**

```bash
python -m pytest tests/test_validate.py -v
```

Expected: `ModuleNotFoundError: No module named 'validate_kie'`

- [ ] **Step 3: Implement validate_kie.py**

Create `scripts/validate_kie.py`:

```python
#!/usr/bin/env python3
"""
KIE Blog Archive Validator
Phase 4: checks all saved posts for broken images, links, and missed transforms.

Usage:
    python scripts/validate_kie.py --legacy legacy
"""
import argparse
import json
import sys
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).parent))


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
        rel = href.replace('../../', '')
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

    by_type = {}
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
```

- [ ] **Step 4: Run tests**

```bash
python -m pytest tests/test_validate.py -v
```

Expected: 4 tests PASS.

- [ ] **Step 6: Commit**

```bash
git add scripts/validate_kie.py tests/test_validate.py
git commit -m "feat: validation pass for images, links, and unreplaced gists"
```

---

## Task 13: Index Generation

**Files:**
- Create: `scripts/generate_index.py`
- Create: `tests/test_generate_index.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_generate_index.py`:

```python
import sys, json, tempfile
from pathlib import Path
sys.path.insert(0, 'scripts')
from generate_index import load_all_sidecars, group_by_author, render_index


def _write_sidecar(directory, filename, data):
    p = directory / filename
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data))
    return p


SIDECAR_A = {
    'title': 'Post A', 'author': 'Mark Proctor', 'author_slug': 'mark-proctor',
    'date': '2022-07-29', 'categories': ['Rules'], 'tags': [],
    'original_url': 'https://blog.kie.org/2022/07/post-a.html',
}
SIDECAR_B = {
    'title': 'Post B', 'author': 'Mark Proctor', 'author_slug': 'mark-proctor',
    'date': '2023-01-10', 'categories': ['AI'], 'tags': [],
    'original_url': 'https://blog.kie.org/2023/01/post-b.html',
}
SIDECAR_C = {
    'title': 'Post C', 'author': 'Jane Smith', 'author_slug': 'jane-smith',
    'date': '2023-05-01', 'categories': ['Tools'], 'tags': [],
    'original_url': 'https://blog.kie.org/2023/05/post-c.html',
}


def test_load_all_sidecars(tmp_path):
    posts_dir = tmp_path / 'posts'
    _write_sidecar(posts_dir / 'mark-proctor', '2022-07-29-post-a.json', SIDECAR_A)
    _write_sidecar(posts_dir / 'jane-smith', '2023-05-01-post-c.json', SIDECAR_C)
    sidecars = load_all_sidecars(tmp_path)
    assert len(sidecars) == 2


def test_group_by_author_keys():
    grouped = group_by_author([SIDECAR_A, SIDECAR_B, SIDECAR_C])
    assert 'mark-proctor' in grouped
    assert 'jane-smith' in grouped


def test_group_by_author_sorted_by_date_desc():
    grouped = group_by_author([SIDECAR_A, SIDECAR_B])
    proctor_posts = grouped['mark-proctor']
    assert proctor_posts[0]['date'] > proctor_posts[1]['date']


def test_render_index_contains_authors():
    grouped = group_by_author([SIDECAR_A, SIDECAR_B, SIDECAR_C])
    html = render_index(grouped, total=3, archived_date='2026-04-01')
    assert 'Mark Proctor' in html
    assert 'Jane Smith' in html


def test_render_index_contains_titles():
    grouped = group_by_author([SIDECAR_A])
    html = render_index(grouped, total=1, archived_date='2026-04-01')
    assert 'Post A' in html


def test_render_index_no_external_resources():
    grouped = group_by_author([SIDECAR_A])
    html = render_index(grouped, total=1, archived_date='2026-04-01')
    assert 'cdn.' not in html
    assert 'googleapis' not in html
    assert '<script' not in html
```

- [ ] **Step 2: Run to confirm failure**

```bash
python -m pytest tests/test_generate_index.py -v
```

Expected: `ModuleNotFoundError: No module named 'generate_index'`

- [ ] **Step 3: Implement generate_index.py**

Create `scripts/generate_index.py`:

```python
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
from pathlib import Path


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
            date = html_module.escape(post.get('date', ''))
            title = html_module.escape(post.get('title', 'Untitled'))
            post_slug = post.get('original_url', '').rstrip('/').split('/')[-1].replace('.html', '')
            post_date = post.get('date', '0000-00-00')
            local_href = f"posts/{author_slug}/{post_date}-{post_slug}.html"
            cats = ' '.join(
                f'<span class="badge">{html_module.escape(c)}</span>'
                for c in post.get('categories', [])
            )
            rows.append(
                f'<tr><td class="date">{date}</td>'
                f'<td><a href="{html_module.escape(local_href)}">{title}</a> {cats}</td></tr>'
            )
        author_sections.append(f"""
<section>
  <h2 id="{html_module.escape(author_slug)}">{author_name} <small>({len(posts)} posts)</small></h2>
  <table><tbody>
  {''.join(rows)}
  </tbody></table>
</section>""")

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
    .badge {{ background: #eef; color: #336; font-size: 0.75em; padding: 1px 6px;
              border-radius: 3px; margin-left: 4px; }}
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
{''.join(f'<a href="#{html_module.escape(slug)}">{html_module.escape(posts[0].get("author", slug))} ({len(posts)})</a>' for slug, posts in grouped.items())}
</nav>
{''.join(author_sections)}
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description='Generate KIE archive index page')
    parser.add_argument('--legacy', default='legacy')
    args = parser.parse_args()

    legacy_dir = Path(args.legacy)
    from datetime import date
    sidecars = load_all_sidecars(legacy_dir)
    print(f"Loaded {len(sidecars)} post sidecars.")
    grouped = group_by_author(sidecars)
    html = render_index(grouped, total=len(sidecars), archived_date=str(date.today()))
    out = legacy_dir / 'index.html'
    out.write_text(html, encoding='utf-8')
    print(f"Index written to {out}")


if __name__ == '__main__':
    main()
```

- [ ] **Step 4: Run tests**

```bash
python -m pytest tests/test_generate_index.py -v
```

Expected: 6 tests PASS.

- [ ] **Step 5: Run full test suite**

```bash
python -m pytest tests/ -v
```

Expected: all tests PASS.

- [ ] **Step 6: Commit**

```bash
git add scripts/generate_index.py tests/test_generate_index.py
git commit -m "feat: index generator — browsable HTML index grouped by author"
```

---

## Task 14: Phase 1 — Run wget Mirror

This task runs the actual download. Requires internet access. **Do not run inside the git worktree** — run from the repo root.

- [ ] **Step 1: Confirm wget is installed**

```bash
wget --version
```

Expected: `GNU Wget 1.x.x` (or similar). If missing on macOS: `brew install wget`.

- [ ] **Step 2: Run wget mirror (HTML only)**

From the repo root (not from `legacy/`):

```bash
wget \
  --mirror \
  --no-parent \
  --wait=1 \
  --random-wait \
  --tries=3 \
  --retry-connrefused \
  --user-agent="Mozilla/5.0 (compatible; KIE-Archive/1.0)" \
  --reject "*.css,*.js,*.woff,*.woff2,*.ttf,*.eot,*.png,*.jpg,*.jpeg,*.gif,*.svg,*.ico,*.json,*.xml,*.rss,*.atom,*.zip,*.pdf" \
  --directory-prefix=kie-mirror \
  https://blog.kie.org
```

This will run for **30–60 minutes** given the `--wait=1 --random-wait` flags. You can monitor progress with:

```bash
ls kie-mirror/blog.kie.org/ | head -20
du -sh kie-mirror/
```

Expected final size: ~300–400 MB.

- [ ] **Step 3: Verify mirror structure**

```bash
find kie-mirror/blog.kie.org -name "*.html" | grep -E '/[0-9]{4}/[0-9]{2}/' | wc -l
```

Expected: 1,700–2,000+ files matching the post URL pattern.

---

## Task 15: Phase 2 — Run Extraction (Test Run)

- [ ] **Step 1: Run on 10 posts first**

```bash
python scripts/extract_kie.py \
  --mirror kie-mirror/blog.kie.org \
  --legacy legacy \
  --state ._state.json \
  --limit 10
```

- [ ] **Step 2: Inspect output**

```bash
ls legacy/posts/
ls legacy/posts/$(ls legacy/posts/ | head -1)/
```

Open one of the generated HTML files in a browser and verify:
- Article content is readable
- Images display (not broken)
- No WordPress navigation/sidebar visible
- Archive header shows original URL

- [ ] **Step 3: Check needs-review.json if it exists**

```bash
cat legacy/needs-review.json 2>/dev/null || echo "No issues found"
```

**If items appear here, stop and report them to the user before proceeding.**

- [ ] **Step 4: Run full extraction**

Only proceed if the test run looks good:

```bash
python scripts/extract_kie.py \
  --mirror kie-mirror/blog.kie.org \
  --legacy legacy \
  --state ._state.json
```

This will run for 2–4 hours. Monitor with:

```bash
wc -l <(cat ._state.json | python3 -c "import sys,json; s=json.load(sys.stdin); print(len(s['completed']))")
```

- [ ] **Step 5: After completion, report summary**

```bash
python3 -c "
import json
s = json.load(open('._state.json'))
print(f'Completed: {len(s[\"completed\"])}')
print(f'Failed: {len(s[\"failed\"])}')
"
```

---

## Task 16: Phase 4 — Validation Pass

- [ ] **Step 1: Run validator (skip external links first for speed)**

```bash
python scripts/validate_kie.py --legacy legacy --skip-external
```

Review output. Fix any `missing_image` issues by re-running the extractor (it will retry failed items).

- [ ] **Step 2: Run with external link check**

```bash
python scripts/validate_kie.py --legacy legacy
```

Expected output:
```
Validating 1800 posts...
Validation complete. N issues found.
Report saved to legacy/validation-report.json
```

- [ ] **Step 3: Review report**

```bash
python3 -c "
import json
r = json.load(open('legacy/validation-report.json'))
print(json.dumps(r['summary'], indent=2))
"
```

Report back to user with summary before any further steps.

---

## Task 17: Phase 5 — Generate Index

- [ ] **Step 1: Generate index**

```bash
python scripts/generate_index.py --legacy legacy
```

Expected:
```
Loaded 1800 post sidecars.
Index written to legacy/index.html
```

- [ ] **Step 2: Open index in browser**

```bash
open legacy/index.html
```

Verify:
- All authors appear with post counts
- Links to individual posts work
- Category badges display
- No external resources loading (fully offline)

- [ ] **Step 3: Commit scripts (not legacy/ content)**

```bash
git add scripts/
git commit -m "feat: complete KIE blog archive scripts (extractor, validator, index)"
```
