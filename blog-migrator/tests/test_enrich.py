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
