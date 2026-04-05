"""Tests for enrich.py and enrichment state tracking."""
import sys
from pathlib import Path

# conftest.py sets up sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts import state as State
from bs4 import BeautifulSoup
from unittest.mock import MagicMock, patch


def parse(html: str):
    return BeautifulSoup(f'<article>{html}</article>', 'lxml').find('article')


def _tmp_state(tmp_path):
    p = tmp_path / 'state.json'
    p.write_text('{}')
    State.set_state_file(p)
    return p


def test_mark_enriched_stores_stats(tmp_path):
    _tmp_state(tmp_path)
    State.update('my-post', {'slug': 'my-post', 'ingested_at': '2026-01-01'})
    State.mark_enriched('my-post', {
        'youtube_replaced': 2,
        'gists_replaced': 1,
        'gists_failed': 0,
        'classes_normalised': 5,
        'languages_detected': 3,
        'embeds_wrapped': 1,
    })
    entry = State.get('my-post')
    assert entry['enriched']['youtube_replaced'] == 2
    assert entry['enriched']['gists_replaced'] == 1
    assert 'generated_at' in entry['enriched']


# ── YouTube ───────────────────────────────────────────────────────────────────

def test_youtube_iframe_replaced(tmp_path):
    from enrich import replace_youtube_embeds
    article = parse('<iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ" width="560"></iframe>')
    assets_dir = tmp_path / 'assets'
    assets_dir.mkdir()

    with patch('enrich.requests') as mock_req:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.content = b'FAKEJPEG'
        mock_req.get.return_value = mock_resp
        stats = replace_youtube_embeds(article, assets_dir, mock_req)

    assert article.find('iframe') is None
    fig = article.find('figure', class_='video-embed')
    assert fig is not None
    img = fig.find('img')
    assert img is not None
    assert 'dQw4w9WgXcQ' in img['src']
    assert stats['youtube_replaced'] == 1
    assert (assets_dir / 'yt_dQw4w9WgXcQ.jpg').exists()


def test_youtube_nocookie_replaced(tmp_path):
    from enrich import replace_youtube_embeds
    article = parse('<iframe src="https://www.youtube-nocookie.com/embed/abc123"></iframe>')
    assets_dir = tmp_path / 'assets'
    assets_dir.mkdir()

    with patch('enrich.requests') as mock_req:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.content = b'FAKEJPEG'
        mock_req.get.return_value = mock_resp
        stats = replace_youtube_embeds(article, assets_dir, mock_req)

    assert stats['youtube_replaced'] == 1


def test_non_youtube_iframe_untouched(tmp_path):
    from enrich import replace_youtube_embeds
    article = parse('<iframe src="https://example.com/embed"></iframe>')
    assets_dir = tmp_path / 'assets'
    assets_dir.mkdir()

    with patch('enrich.requests') as mock_req:
        stats = replace_youtube_embeds(article, assets_dir, mock_req)

    assert article.find('iframe') is not None
    assert stats['youtube_replaced'] == 0


def test_youtube_thumbnail_fallback(tmp_path):
    from enrich import replace_youtube_embeds
    article = parse('<iframe src="https://www.youtube.com/embed/abc123"></iframe>')
    assets_dir = tmp_path / 'assets'
    assets_dir.mkdir()

    with patch('enrich.requests') as mock_req:
        not_found = MagicMock()
        not_found.status_code = 404
        ok = MagicMock()
        ok.status_code = 200
        ok.content = b'FAKEJPEG'
        mock_req.get.side_effect = [not_found, ok]
        stats = replace_youtube_embeds(article, assets_dir, mock_req)

    assert stats['youtube_replaced'] == 1


# ── Gists ─────────────────────────────────────────────────────────────────────

GIST_API_RESPONSE = {
    'files': {
        'example.java': {
            'filename': 'example.java',
            'language': 'Java',
            'content': 'public class Foo {}',
        }
    }
}


def test_gist_script_replaced_with_code(tmp_path):
    from enrich import replace_gist_embeds
    article = parse('<script src="https://gist.github.com/mproctor/abc123.js"></script>')

    with patch('enrich.requests') as mock_req:
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = GIST_API_RESPONSE
        mock_req.get.return_value = resp
        stats = replace_gist_embeds(article, '', mock_req)

    assert article.find('script') is None
    fig = article.find('figure', class_='gist-embed')
    assert fig is not None
    code = fig.find('code')
    assert code is not None
    assert 'public class Foo' in code.get_text()
    assert stats['gists_replaced'] == 1
    assert stats['gists_failed'] == 0


def test_gist_api_failure_produces_fallback(tmp_path):
    from enrich import replace_gist_embeds
    article = parse('<script src="https://gist.github.com/mproctor/abc123.js"></script>')

    with patch('enrich.requests') as mock_req:
        resp = MagicMock()
        resp.status_code = 404
        mock_req.get.return_value = resp
        stats = replace_gist_embeds(article, '', mock_req)

    assert article.find('script') is None
    fig = article.find('figure', class_='gist-embed')
    assert fig is not None
    assert 'gist.github.com' in str(fig)
    assert stats['gists_failed'] == 1


def test_gist_uses_github_token(tmp_path):
    from enrich import replace_gist_embeds
    article = parse('<script src="https://gist.github.com/abc123.js"></script>')

    with patch('enrich.requests') as mock_req:
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = GIST_API_RESPONSE
        mock_req.get.return_value = resp
        replace_gist_embeds(article, 'ghp_mytoken', mock_req)

    call_kwargs = mock_req.get.call_args[1]
    assert 'Authorization' in call_kwargs.get('headers', {})
    assert 'ghp_mytoken' in call_kwargs['headers']['Authorization']


def test_non_gist_script_untouched():
    from enrich import replace_gist_embeds
    article = parse('<script src="https://example.com/analytics.js"></script>')

    with patch('enrich.requests') as mock_req:
        stats = replace_gist_embeds(article, '', mock_req)

    assert article.find('script') is not None
    assert stats['gists_replaced'] == 0
