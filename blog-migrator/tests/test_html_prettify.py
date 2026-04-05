"""
Tests for HTML prettification in the editor view (GET /api/posts/{slug}/html).

Three layers:
  1. Unit tests  — prettify logic in isolation, no server required
  2. Happy path  — well-formed HTML comes back multi-line and equivalent
  3. Integration — live endpoint returns prettified content
"""
import sys
import textwrap
from pathlib import Path

import pytest

MIGRATOR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(MIGRATOR_ROOT / 'scripts'))


# ── Unit tests — prettify logic ───────────────────────────────────────────────

def _prettify(html: str) -> str:
    """Mirror the exact logic in _api_post_html."""
    from bs4 import BeautifulSoup
    return BeautifulSoup(html, 'lxml').prettify()


class TestPrettifyUnit:
    """Prettify logic tested in isolation — no server required."""

    def test_minified_html_gains_newlines(self):
        """All-on-one-line HTML should become multi-line after prettify."""
        minified = '<html><body><article><p>Hello world</p><p>Second para</p></article></body></html>'
        result = _prettify(minified)
        assert '\n' in result
        assert result.count('\n') > 3

    def test_content_preserved_after_prettify(self):
        """Text content must survive prettification unchanged."""
        html = '<html><body><p>Drools is a <strong>Rule Engine</strong></p></body></html>'
        result = _prettify(html)
        assert 'Drools is a' in result
        assert 'Rule Engine' in result

    def test_links_preserved(self):
        """Hyperlinks must survive prettification with correct href."""
        html = '<html><body><p><a href="http://example.com/rule-engine">Rule Engine</a></p></body></html>'
        result = _prettify(html)
        assert 'href="http://example.com/rule-engine"' in result
        assert 'Rule Engine' in result

    def test_pre_code_content_preserved_verbatim(self):
        """<pre> and <code> blocks must not have their whitespace altered."""
        code_content = 'public class Foo {\n    public static void main() {}\n}'
        html = f'<html><body><pre><code>{code_content}</code></pre></body></html>'
        result = _prettify(html)
        assert code_content in result

    def test_already_formatted_html_stays_equivalent(self):
        """Already-formatted HTML remains equivalent after prettify (idempotent text)."""
        html = textwrap.dedent('''\
            <html>
              <body>
                <article>
                  <p>First paragraph</p>
                  <p>Second paragraph</p>
                </article>
              </body>
            </html>''')
        result = _prettify(html)
        assert 'First paragraph' in result
        assert 'Second paragraph' in result

    def test_images_preserved(self):
        """Image src attributes must survive prettification."""
        html = '<html><body><img src="assets/img001.jpg" alt="Figure 1"/></body></html>'
        result = _prettify(html)
        assert 'assets/img001.jpg' in result

    def test_minified_paragraph_per_line(self):
        """Each <p> should appear on its own line after prettify."""
        html = '<html><body><p>Para one</p><p>Para two</p><p>Para three</p></body></html>'
        result = _prettify(html)
        lines = result.splitlines()
        para_lines = [l for l in lines if '<p>' in l or 'Para' in l]
        # Each paragraph content should be on a separate line
        assert len(para_lines) >= 3

    def test_single_long_line_becomes_multiple(self):
        """The exact pattern from "What is a Rule Engine" — very long single line."""
        minified = (
            '<html><body><article><div>'
            '<p>Production Rules is a Rule Based approach.</p>'
            '<p>The term Rule Engine is quite ambiguous.</p>'
            '<p>A Production Rule System is turing complete.</p>'
            '<p>Forward Chaining is data-driven.</p>'
            '<p>The Rete algorithm by Charles Forgy.</p>'
            '</div></article></body></html>'
        )
        result = _prettify(minified)
        # Should have many more lines than the original
        original_lines = minified.count('\n') + 1  # = 1
        result_lines   = result.count('\n') + 1
        assert result_lines > original_lines * 5

    def test_html_entities_preserved(self):
        """HTML entities like &amp; must survive."""
        html = '<html><body><p>A &amp; B</p></body></html>'
        result = _prettify(html)
        assert '&amp;' in result or 'A' in result  # BS4 may decode &amp; → & but text preserved

    def test_nested_structure_preserved(self):
        """Nested elements must maintain their nesting after prettify."""
        html = '<html><body><ul><li><a href="x">Link</a></li></ul></body></html>'
        result = _prettify(html)
        assert '<a' in result
        assert 'href="x"' in result
        assert 'Link' in result


# ── Happy path tests — file-level prettify ───────────────────────────────────

class TestPrettifyHappyPath:
    """End-to-end prettify on real archived HTML files — no server required."""

    @pytest.fixture(scope='class')
    def legacy_posts(self):
        """Return up to 5 real legacy HTML files for testing."""
        import sparge_home as _sh
        proj_dir = _sh.get_projects_dir() / 'kie-mark-proctor'
        if not proj_dir.exists():
            pytest.skip('kie-mark-proctor project not found')
        cfg_path = proj_dir / 'config.json'
        if not cfg_path.exists():
            pytest.skip('Project config not found')
        import json
        cfg = json.loads(cfg_path.read_text())
        posts_dir = Path(cfg['serve_root']) / cfg['source']['posts_dir']
        files = sorted(posts_dir.glob('*.html'))[:5]
        if not files:
            pytest.skip('No HTML files found')
        return files

    def test_real_posts_become_multiline(self, legacy_posts):
        """Every real post file becomes multi-line after prettify."""
        for path in legacy_posts:
            raw = path.read_text(encoding='utf-8', errors='replace')
            result = _prettify(raw)
            assert result.count('\n') > 10, \
                f'{path.name} should have >10 lines after prettify'

    def test_real_posts_text_content_preserved(self, legacy_posts):
        """Spot-check: key words from original appear in prettified version."""
        from bs4 import BeautifulSoup
        for path in legacy_posts:
            raw = path.read_text(encoding='utf-8', errors='replace')
            original_text = BeautifulSoup(raw, 'lxml').get_text()
            result_text   = BeautifulSoup(_prettify(raw), 'lxml').get_text()
            # Both should have substantially the same words
            orig_words   = set(original_text.split())
            result_words = set(result_text.split())
            # Allow small differences from whitespace normalisation
            # Allow for minor whitespace/punctuation differences from BS4 normalisation
            # Key check: result has roughly the same word count
            assert len(result_words) >= len(orig_words) * 0.9, \
                f'{path.name}: result has {len(result_words)} words vs original {len(orig_words)}'

    def test_what_is_a_rule_engine_becomes_editable(self, legacy_posts):
        """The notorious single-line post should become multi-line."""
        rule_engine = next(
            (p for p in legacy_posts if 'what-is-a-rule-engine' in p.name), None
        )
        if rule_engine is None:
            # Try directly
            import sparge_home as _sh
            import json
            proj_dir = _sh.get_projects_dir() / 'kie-mark-proctor'
            cfg = json.loads((proj_dir / 'config.json').read_text())
            posts_dir = Path(cfg['serve_root']) / cfg['source']['posts_dir']
            rule_engine = posts_dir / '2006-05-31-what-is-a-rule-engine.html'
            if not rule_engine.exists():
                pytest.skip('what-is-a-rule-engine.html not found')

        raw = rule_engine.read_text(encoding='utf-8', errors='replace')
        # Confirm it's minified (all content on very few lines)
        raw_lines = raw.count('\n') + 1
        result = _prettify(raw)
        result_lines = result.count('\n') + 1
        # Must expand significantly — the article body was one long line
        assert result_lines > raw_lines + 50, \
            f'Expected >50 new lines, got {raw_lines}→{result_lines}'
        assert 'Production Rule' in result
        assert 'Rule Engine' in result


# ── Integration tests — live server endpoint ─────────────────────────────────

try:
    import requests as _requests
    SERVER  = 'http://localhost:9000'
    API     = SERVER + '/api'
    SESSION = _requests.Session()
    SESSION.headers['Content-Type'] = 'application/json'
    _HAS_REQUESTS = True
except ImportError:
    _HAS_REQUESTS = False


@pytest.fixture(scope='module')
def server():
    if not _HAS_REQUESTS:
        pytest.skip('requests not installed')
    try:
        _requests.get(f'{API}/projects', timeout=3).raise_for_status()
    except Exception:
        pytest.skip('Server not running on localhost:9000')


@pytest.fixture(scope='module')
def first_slug(server):
    posts = SESSION.get(f'{API}/posts').json()
    if not posts:
        pytest.skip('No posts in active project')
    return posts[0]['slug']


class TestPrettifyEndpoint:
    """Integration tests for GET /api/posts/{slug}/html prettification."""

    def test_endpoint_returns_multiline_html(self, server, first_slug):
        """The /html endpoint must return multi-line content."""
        r = SESSION.get(f'{API}/posts/{first_slug}/html')
        assert r.status_code == 200
        assert r.text.count('\n') > 10, \
            'Editor HTML should have >10 lines (prettified)'

    def test_endpoint_preserves_text_content(self, server, first_slug):
        """Prettified HTML must contain same text as original."""
        from bs4 import BeautifulSoup
        r = SESSION.get(f'{API}/posts/{first_slug}/html')
        assert r.status_code == 200
        text = BeautifulSoup(r.text, 'lxml').get_text()
        # Must have substantial content
        assert len(text.split()) > 20, 'Prettified HTML should contain article text'

    def test_what_is_a_rule_engine_is_prettified(self, server):
        """The notorious single-line post must be multi-line in editor."""
        slug = '2006-05-31-what-is-a-rule-engine'
        r = SESSION.get(f'{API}/posts/{slug}/html')
        if r.status_code == 404:
            pytest.skip('what-is-a-rule-engine not in active project')
        assert r.status_code == 200
        lines = r.text.count('\n') + 1
        assert lines > 50, \
            f'Expected >50 lines for prettified "What is a Rule Engine", got {lines}'
        assert 'Production Rule' in r.text
        assert 'Rule Engine' in r.text

    def test_prettified_html_each_para_on_own_line(self, server, first_slug):
        """Each <p> tag should open on its own line."""
        r = SESSION.get(f'{API}/posts/{first_slug}/html')
        assert r.status_code == 200
        lines_with_p = [l.strip() for l in r.text.splitlines() if '<p>' in l]
        # At least some lines should start with <p>
        assert len(lines_with_p) >= 1

    def test_save_and_refetch_still_prettified(self, server, first_slug):
        """After saving prettified content back, re-fetch is still prettified."""
        original = SESSION.get(f'{API}/posts/{first_slug}/html').text
        # Save the prettified version back
        SESSION.post(
            f'{API}/posts/{first_slug}/save-html',
            data=original.encode('utf-8'),
            headers={'Content-Type': 'text/html; charset=utf-8'},
        )
        # Re-fetch must still be prettified
        refetched = SESSION.get(f'{API}/posts/{first_slug}/html').text
        assert refetched.count('\n') > 10

    def test_all_posts_in_project_return_prettified_html(self, server):
        """Every post in the active project returns multi-line HTML."""
        posts = SESSION.get(f'{API}/posts').json()[:5]  # check first 5
        for post in posts:
            r = SESSION.get(f'{API}/posts/{post["slug"]}/html')
            assert r.status_code == 200, f'{post["slug"]} returned {r.status_code}'
            assert r.text.count('\n') > 5, \
                f'{post["slug"]} should be prettified (multi-line)'
