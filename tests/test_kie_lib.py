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
