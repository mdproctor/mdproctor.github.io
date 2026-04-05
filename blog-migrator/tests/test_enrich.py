"""Tests for enrich.py and enrichment state tracking."""
import sys
from pathlib import Path

# conftest.py sets up sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts import state as State


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
