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
